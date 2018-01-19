from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import Message, Attachment
from app.forms import MessageForm, AttachmentForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'


class MessageView(LoginRequiredMixin, View):
    model = Message

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=pk)
            attachment = Attachment.objects.filter(message=instance)
            if self.request.user in instance.recivers:
                return render(request, 'inbox/message_details.html', {'instance': instance,
                                                                      'attachment': attachment})
            elif instance.sender == self.request.user:
                return render(request, 'inbox/message_details.html', {'instance': instance,
                                                                      'attachment': attachment,
                                                                      'sent': True})


            return HttpResponseRedirect('/inbox/')
        except:
            return HttpResponseRedirect('/inbox/')


class MessageFormView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        asd = request.POST.copy()
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.save()
            form.save_m2m()
            if len(request.FILES.getlist('file_object')) > 0:
                for a in request.FILES.getlist('file_object'):
                    attachment = Attachment.objects.create(file_object=a)
                    attachment.message.add(instance)
                    attachment.save()
                
            return HttpResponseRedirect('/inbox/messages/{}'.format(instance.pk))
    
    def get(self, request, *args, **kwargs):
        form = MessageForm(request.GET)
        return render(request, 'inbox/message_form.html', {'form': form})


class MessageReplyView(MessageFormView):
    def get(self, request, pk, *args, **kwargs):
        msg = Message.objects.get(pk=pk)
        attachment = Attachment.objects.filter(message=msg)
        form = MessageForm(request.GET)
        if msg.sender == self.request.user or self.request.user in msg.recivers:
            return render(request, 'inbox/message_form.html', {'form': form, 'reply': msg, 'attachment': attachment})
        return HttpResponseRedirect('/inbox/')

class MessageResendView(MessageFormView):
    def get(self, request, pk, *args, **kwargs):
        msg = Message.objects.get(pk=pk)
        attachment = Attachment.objects.filter(message=msg)
        form = MessageForm(request.GET)
        if msg.sender == self.request.user or self.request.user in msg.recivers:
            return render(request, 'inbox/message_form.html', {'form': form, 'resend': msg, 'attachment': attachment})
        return HttpResponseRedirect('/inbox/')

    def post(self, request, pk, *args, **kwargs):
        asd = request.POST.copy()
        form = MessageForm(asd, request.FILES)
        print(form.errors)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.save()
            form.save_m2m()
            # new attachments
            for a in request.FILES.getlist('file_object'):
                if a:
                    attachment = Attachment.objects.create(file_object=a)
                    attachment.message.add(instance)
                    attachment.save()
            # old attachments
            if Attachment.objects.filter(message=pk).exists:
               for x in Attachment.objects.filter(message=pk):
                   x.message.add(instance)
                   x.save()

                
            return HttpResponseRedirect('/inbox/messages/{}'.format(instance.pk))

class UploadAttachmentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        attachments = Attachment.objects.all()
        return render(request, 'attachments/upload.html', {'attachments': attachments})

    def post(self, request, *args, **kwargs):
        form = AttachmentForm(request.POST, request.FILES)
        response = []
        if form.is_valid():
            for a in request.FILES.getlist('file_object'):
                attachment = Attachment(file_object=a, name=a.file_object.name)
                attachment.save()
                response.append({'is_valid': True, 'name': attachment.file_object.name,
                                 'url': attachment.file_object.url})
        else:
            data = {'is_valid': False}
        return JsonResponse(json.dumps(response))


class InboxView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'recived_messages'
    template_name = 'inbox/inbox.html'

    def get_queryset(self):
        print(self.request.user)
        return Message.objects.filter(recivers=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_messages'] = Message.objects.filter(sender=self.request.user, delete_for_sender=False)
        return context


class MessageDeleteView(LoginRequiredMixin, View):
    template_name = 'inbox/inbox.html'
    
    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.recivers.remove(request.user.id)
        return redirect('inbox')


class SendMessageDeleteView(LoginRequiredMixin, View):
    template_name = 'inbox/inbox.html'

    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.delete_for_sender = True
        message.save()
        return redirect('inbox')