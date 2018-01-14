from django import forms
from app.models import Attachment, Message


class MessageForm(forms.ModelForm):
    file_object = forms.FileField(required=False)

    class Meta:
        model = Message
        fields = ('subject', 'recivers', 'body',)


class AttachmentForm(forms.ModelForm):
    file_object = forms.FileField(required=False)

    class Meta:
        model = Attachment
        fields = ('file_object', 'name',)