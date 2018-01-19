from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Temat')
    recivers = models.ManyToManyField('auth.User', blank=True)
    sender = models.ForeignKey('auth.User', on_delete='ignore', related_name='sender', null=True, blank=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    delete_for_sender = models.BooleanField(default=False, blank=True)


class Attachment(models.Model):
    message = models.ManyToManyField('app.Message', null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    file_object = models.FileField(upload_to='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
