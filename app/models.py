from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Temat')
    users = models.ManyToManyField('auth.User')
    attachments = models.ManyToManyField('app.Attachment')
    body = models.TextField()


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    file_object = models.FileField(upload_to='static/')
    uploaded_at = models.DateTimeField(auto_now_add=True)