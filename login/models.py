from django.db import models


# Create your models here.
class User(models.Model):
    gender = (('male', '男'), ('female', '女'))
    name = models.CharField(max_length=60, verbose_name='用户名')
    sex = models.CharField(max_length=60, choices=gender, default=gender[0], verbose_name='性别')
    password = models.CharField(max_length=60, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    c_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '用户'
        verbose_name_plural = '用户们'
