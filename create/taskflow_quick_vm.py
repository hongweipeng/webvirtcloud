import os
import random
from django.utils import timezone
from vrtManager import taskflow_base
from vrtManager import consts, util
from vrtManager.create import wvmCreate
from vrtManager.hostdetails import wvmHostDetails
from vrtManager.storage import wvmStorage
from vrtManager.instance import wvmInstance
from create import models as create_models
from computes import models as compute_models
from instances.models import Instance
from libvirt import libvirtError

class ClearIfSet(taskflow_base.TaskBase):
    def do_execute(self, quick_model:create_models.QuickVM):
        if not quick_model.instance:
            return None

        if not quick_model.compute_id or not compute_models.Compute.objects.filter(id=quick_model.compute_id).exists():
            return None
        instance = quick_model.instance
        compute = compute_models.Compute.objects.get(id=quick_model.compute_id)
        # 做一些清理工作
        conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           quick_model.instance.name)
        status = conn.get_status()

        # 状态为 5 ，表示关闭，可以删除
        if status != 5:
            raise Exception('%s is not shutdwon in host %s' % (quick_model.instance.name, compute.name))

        snapshots = sorted(conn.get_snapshot(), reverse=True, key=lambda k:k['date'] )
        for snap in snapshots:
            conn.snapshot_delete(snap['name'])
        conn.delete_disk()
        conn.delete()
        conn.close()
        instance.delete()
        quick_model.refresh_from_db()

class ValidTemplateCode(taskflow_base.TaskBase):
    """验证实验镜像是否已认证"""
    def do_execute(self, raw_model:create_models.QuickVM):
        pass
            
class SelectCompute(taskflow_base.TaskBase):
    """
    寻找有足够资源存放vm的机器
    """
    def do_execute(self, quick_model:create_models.QuickVM):
        error_messages = []
        select_compute = None
        
        # vm需要的系统资源
        vcpu_num = quick_model.template.vcpu
        memory = quick_model.template.memory
        
        
        all_computes = list(compute_models.Compute.objects.all())
        random.shuffle(all_computes)
        for compute in all_computes:
            try:
                conn = wvmHostDetails(compute.hostname,
                                      compute.login,
                                      compute.password,
                                      compute.type)
                hostname, host_arch, host_memory, logical_cpu, model_cpu, uri_conn = conn.get_node_info()
                # hypervisor = conn.hypervisor_type()
                mem_usage = conn.get_memory_usage()
                conn.close()
                if logical_cpu < vcpu_num:  # 宿主上的逻辑cpu数量不满足要求
                    continue
                if (host_memory - mem_usage['usage']) // 1048576 < memory:    # 宿主剩余内存空间不满足要求
                    continue
                
                quick_model.compute_id = compute.id
                select_compute = compute
                quick_model.save()
                break
            except libvirtError as lib_err:
                error_messages.append(lib_err)
        else:
            raise Exception('can not find idle compute for %s' % quick_model.token)
        
        return select_compute.name

class CreateDisk(taskflow_base.TaskBase):
    """
    创建磁盘
    """
    backing_pool_name = 'backing'
    target_disk_pool_name = 'imgdev'
    disk_format = 'qcow2'
    
    def do_execute(self, quick_model: create_models.QuickVM):
        disks_path = []
        compute = compute_models.Compute.objects.get(id=quick_model.compute_id)
        conn = wvmStorage(compute.hostname,
                          compute.login,
                          compute.password,
                          compute.type,
                          self.target_disk_pool_name)
        
        pool_dir = util.get_xml_path(conn.pool.XMLDesc(), 'target/path')
        backing_file = quick_model.template.backing_file
        if backing_file:
            backing_file = backing_file.name
            backing_pool = conn.get_storage(self.backing_pool_name)

            vol = backing_pool.storageVolLookupByName(backing_file)
            backing_file = vol.path()   # 绝对路径
            meta_prealloc = False
            disk_name = quick_model.token + '-backing'
            
            data = {
                'name': disk_name,
                'size': 1, # GB     后端镜像不需要指定磁盘大小
                'format': self.disk_format,
                'is_use_backing': True,
            }
            conn.create_volume(data['name'], data['size'], data['format'], meta_prealloc, data["is_use_backing"],
                               backing_file)
            disks_path.append(os.path.join(pool_dir, '%s.%s' % (disk_name, self.disk_format)))

        # 创建数据盘
        if quick_model.template.disk:
            disks = [ x.strip() for x in quick_model.template.disk.split(',')]
            for i, disk in enumerate(disks, start=1):
                meta_prealloc = False
                disk_name = quick_model.token + '-disk' + str(i)
                data = {
                    'name': disk_name,
                    'size': int(disk),  # GB
                    'format': 'qcow2',
                }
                conn.create_volume(data['name'], data['size'], data['format'], meta_prealloc)
                disks_path.append(os.path.join(pool_dir, '%s.%s' % (disk_name, self.disk_format)))
        
        quick_model.disks_path = ','.join(disks_path)
        quick_model.save()
        return quick_model.disks_path
        
        

class CreateVM(taskflow_base.TaskBase):
    """
    创建虚机
    """
    def do_execute(self, quick_model: create_models.QuickVM):
        vcpu_num = quick_model.template.vcpu
        memory = quick_model.template.memory
        clock = quick_model.template.clock
        network = quick_model.template.network
        if not quick_model.disks_path:
            raise Exception('no disk')
        
        compute = compute_models.Compute.objects.get(id=quick_model.compute_id)
        conn = wvmCreate(compute.hostname,
                         compute.login,
                         compute.password,
                         compute.type)
        uuid = util.randomUUID()
        #path = conn.get_volume_path(vol)
        #volumes[path] = conn.get_volume_type(path)
        disks = quick_model.disks_path.split(',')

        
        volumes = {}
        for disk_path in disks:
            volumes[disk_path] = conn.get_volume_type(disk_path)

        data = {
            'uuid': uuid,
            'name': quick_model.token,
            'memory': memory,
            'vcpu': vcpu_num,
            'images': volumes,
            'host_model': True,
            'cache_mode': 'default',
            'networks': network,
            'virtio': True,
            'clock': clock,
        }
        console_type = quick_model.template.video_mode
        conn.create_instance(**data, console_type=console_type, video_model='qxl')
        create_instance = Instance(compute_id=quick_model.compute_id, name=data['name'], uuid=uuid)
        create_instance.save()
        quick_model.instance = create_instance
        quick_model.save()
        
class StarVM(taskflow_base.TaskBase):
    def do_execute(self, quick_model: create_models.QuickVM):
        compute = compute_models.Compute.objects.get(id=quick_model.compute_id)
        
        conn = wvmInstance(compute.hostname,
                           compute.login,
                           compute.password,
                           compute.type,
                           quick_model.instance.name)
        conn.start()
        instance = quick_model.instance
        instance.start_time = timezone.now()
        instance.save()
        return True
        
class Step2(taskflow_base.TaskBase):
    def do_execute(self, raw_model):
        pass



class END(taskflow_base.TaskBase):
    def do_execute(self, raw_model):
        raw_model.status = consts.TASK_FINISH
        raw_model.save()
        print("END")
        return True

STEPS = (
    ClearIfSet,
    SelectCompute,
    CreateDisk,
    CreateVM,
    StarVM,
    #Step2,
    END,
)