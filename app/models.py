from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Temat')
    recivers = models.ManyToManyField('auth.User', blank=True)
    sender = models.ForeignKey('auth.User', on_delete='ignore',
                               related_name='sender', null=True, blank=True)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    delete_for_sender = models.BooleanField(default=False, blank=True)
    readed_by = models.ManyToManyField('auth.User', related_name='reads', blank=True)


class Attachment(models.Model):
    message = models.ManyToManyField('app.Message', null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    file_object = models.FileField(upload_to='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    users = models.ManyToManyField('auth.User', blank=True)
    message = models.ForeignKey('Message', on_delete='ignore', null=True, blank=True)
    body = models.CharField(max_length=255, blank=True)
    readed_by = models.ManyToManyField('auth.User', blank=True, related_name='user')
