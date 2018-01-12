from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Temat')
    recivers = models.ManyToManyField('auth.User')
    sender = models.ForeignKey('auth.User', on_delete='ignore', related_name='sender', null=True, blank=True)
    attachments = models.ManyToManyField('app.Attachment', null=True, blank=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    file_object = models.FileField(upload_to='static/')
    uploaded_at = models.DateTimeField(auto_now_add=True)