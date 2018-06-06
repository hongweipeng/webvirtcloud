from django.db import models


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
    
    virtio = models.BooleanField(default=True)
    
    def __str__(self):
        return self.label
    
    
