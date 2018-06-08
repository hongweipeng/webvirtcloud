from django.db import models
from vrtManager import consts

class Flavor(models.Model):
    label = models.CharField(max_length=12)
    memory = models.IntegerField()
    vcpu = models.IntegerField()
    disk = models.IntegerField()

    def __str__(self):
        return self.label


class BackingFile(models.Model):
    """
    后端镜像，手动录入，要求所有宿主机中要有这个名称的镜像
    """
    label = models.CharField(max_length=31)
    name = models.CharField(max_length=63, verbose_name='镜像文件名称')
    os_type = models.CharField(max_length=31, null=True, blank=True)
    size = models.IntegerField(default=0, verbose_name='大小GB')
    
    def __str__(self):
        return "%s: %s" % (self.label, self.name)
    

class VMTemplate(models.Model):
    label = models.CharField(max_length=31, verbose_name='模板名称')
    vcpu = models.IntegerField(verbose_name='cpu个数')
    memory = models.IntegerField(verbose_name='内存大小MB')
    backing_file = models.ForeignKey(BackingFile, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='后端镜像')
    
    disk = models.CharField(max_length=31, null=True, blank=True, verbose_name='硬盘')

    network = models.CharField(max_length=13, choices=consts.NETWORK_CHOICE, default='default')
    clock = models.CharField(max_length=13, choices=consts.CLOCK_CHOICE, default='utc')
    virtio = models.BooleanField(default=True)
    
    def __str__(self):
        return self.label
    
    
class QuickVM(models.Model):
    """
    快速出机，此表中的记录全部是后端镜像出机
    """
    id = models.AutoField(auto_created=True, primary_key=True)
    credit = models.CharField(max_length=63, unique=True, verbose_name='凭证')
    token = models.CharField(max_length=63, unique=True, verbose_name='token')
    template = models.ForeignKey(VMTemplate, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='模板')
    compute_id = models.IntegerField(default=0, verbose_name='宿主id')
    instance = models.ForeignKey('instances.Instance', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='实例')
    status = models.CharField(max_length=31, null=True, choices=consts.TASK_CHOICE)
    disks_path = models.CharField(max_length=511, null=True, blank=True)
    # 步骤
    step = models.CharField(max_length=31, null=True, blank=True)
    
    def __str__(self):
        return self.token
    
class StepHistoryBase(models.Model):
    """
    单个步骤的部署历史
    """

    name = models.CharField(max_length=31, verbose_name='步骤名称')
    status = models.CharField(max_length=31, choices=consts.HISTORY_STATUS, verbose_name='状态')
    result = models.TextField(null=True, blank=True, verbose_name='详细信息')
    created = models.DateTimeField(auto_now=True, verbose_name='创建日期')
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name
    
class QuickVMStep(StepHistoryBase):
    """
    快速出机的历史步骤
    """
    quick_id = models.IntegerField(default=0)
    def __str__(self):
        return "%s: %s - %s" %(self.quick_id, self.name, self.status)
    