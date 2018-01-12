from django import forms
from app.models import Attachment, Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'recivers', 'body',)

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = '__all__'