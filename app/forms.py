from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app.models import Attachment, Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'recivers', 'body',)

    file_object = forms.FileField(required=False)
    recivers = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.SelectMultiple(attrs={'id': 'recivers', 'name': 'recivers'}))

    def clean(self):
        print(self.cleaned_data)
        return self.cleaned_data


class AttachmentForm(forms.ModelForm):
    file_object = forms.FileField(required=False)

    class Meta:
        model = Attachment
        fields = ('file_object', 'name',)