# -*- coding: utf8 -*-
# linyouyi
from django.db import models

# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    def __str__(self):
        return self.name
class HostGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    def __str__(self):
        return self.name
class Host(models.Model):
    hostname = models.CharField(max_length=32, db_index=True)
    alias = models.CharField(max_length=32,default="alias")
    public_ip = models.GenericIPAddressField(protocol="ipv4", db_index=True)
    private_ip = models.GenericIPAddressField(protocol="ipv4")
    system = models.CharField(max_length=32)
    cpu_version = models.CharField(max_length=32)
    cpu_thread_num = models.SmallIntegerField(default=1)
    memory = models.IntegerField()
    hard_disk = models.IntegerField()
    admin_root = models.CharField(max_length=16)
    admin_pass = models.CharField(max_length=64)
    port = models.CharField(max_length=64)
    status_choice = ((0, 'downline'), (1, 'online'))
    status = models.SmallIntegerField(choices=status_choice, default=0)
    hostgroup = models.ForeignKey("HostGroup", to_field="id", on_delete=True)
    business = models.ForeignKey("Business", to_field="id", on_delete=True)
    def __str__(self):
        return self.hostname

#一个主机可以在多个组,一个组可以拥有多个主机
class HostToHostGroup(models.Model):
    host_id = models.ForeignKey("Host", to_field="id", on_delete=True)
    host_group_id = models.ForeignKey("HostGroup", to_field="id", on_delete=True)

class ExecuteLog(models.Model):
    hostip = models.GenericIPAddressField(protocol="ipv4")
    hostuser = models.CharField(max_length=32)
    # 如果密钥连接的话就不用记录远程主机的密码,因此hostpass可以为空值
    hostpass = models.CharField(max_length=64, null=True, blank=True)
    # 如果是上传操作则没有命令可记录,因此hostcmd可以为空值
    hostcmd = models.CharField(max_length=254, null=True, blank=True)
    excuteuser = models.CharField(max_length=32)
    #执行用户的ip地址
    excuteip = models.GenericIPAddressField(protocol="ipv4", null=True, blank=True)
    # 如果是执行命令的话则没有文件路径可记录,因此filepath可以为值
    filepath= models.CharField(max_length=128, null=True, blank=True)
    executetime = models.DateTimeField(auto_now_add=True)