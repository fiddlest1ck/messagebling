from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Temat')
    attachment = models.ForeignKey('auth.User', on_delete='ignore')
    body = models.TextField()
