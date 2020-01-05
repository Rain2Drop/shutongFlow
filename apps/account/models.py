from django.db import models
from django.contrib.auth.models import AbstractUser
from common.abstract import AbastractModel


class ShutongDept(AbastractModel):
    name = models.CharField(verbose_name=u'部门名称', max_length=100)
    parent = models.IntegerField(verbose_name=u'上级部门', default=0)
    leader = models.CharField(verbose_name=u'部门负责人', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name


class ShutongRole(AbastractModel):
    name = models.CharField(verbose_name=u'角色名称', max_length=100)
    description = models.CharField(verbose_name=u'角色描述', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        verbose_name = "角色"
        verbose_name_plural = verbose_name


class ShutongUser(AbstractUser):
    username = models.CharField(verbose_name=u'用户名', max_length=100, unique=True)
    alias = models.CharField(verbose_name=u'姓名', max_length=100, default='')
    email = models.EmailField(verbose_name=u'邮箱', max_length=100, default='')
    phone = models.CharField(verbose_name=u'电话', max_length=13, default=0)
    dept = models.ForeignKey('ShutongDept', db_column='dept', verbose_name=u'部门', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name=u'己激活', default=True)
    is_superuser = models.BooleanField(verbose_name=u'超级管理员', default=False)
    is_staff = models.BooleanField(verbose_name=u'允许登录admin', default=False)
    created = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    modified = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    deleted = models.BooleanField(verbose_name=u'己删除', default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class ShutongUserRole(AbastractModel):
    user = models.IntegerField(verbose_name=u'用户')
    role = models.IntegerField(verbose_name=u'角色')

    def __str__(self):
        return '{}-{}'.format(self.user, self.role)

    class Meta:
        verbose_name = "用户角色"
        verbose_name_plural = verbose_name
