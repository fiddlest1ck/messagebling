from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import Message, Attachment, Notification
from app.forms import MessageForm, AttachmentForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'


class MessageView(LoginRequiredMixin, View):
    model = Message

    def get(self, request, pk, *args, **kwargs):
        
            instance = self.model.objects.get(pk=pk)
            attachment = Attachment.objects.filter(message=instance)
            if self.request.user in instance.recivers.all():
                instance.readed_by.add(request.user)
                instance.save()
                return render(request, 'inbox/message_details.html', {'instance': instance,
                                                                      'attachment': attachment})
            elif instance.sender == self.request.user:
                instance.readed_by.add(request.user)
                instance.save()
                return render(request, 'inbox/message_details.html', {'instance': instance,
                                                                      'attachment': attachment,
                                                                      'sent': True})


            return HttpResponseRedirect('/inbox/messages/recived')


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
            notification = Notification.objects.create(message=instance)
            notification.users.add(*instance.recivers.all())
            notification.save()
                
            return HttpResponseRedirect('/inbox/messages/recived')
        return render(request, 'inbox/message_form.html', {'form': form})

    
    def get(self, request, *args, **kwargs):
        form = MessageForm(request.GET)
        return render(request, 'inbox/message_form.html', {'form': form})


class MessageReplyView(MessageFormView):
    def get(self, request, pk, *args, **kwargs):
        msg = Message.objects.get(pk=pk)
        attachment = Attachment.objects.filter(message=msg)
        form = MessageForm(request.GET)
        if msg.sender == self.request.user or self.request.user in msg.recivers.all():
            return render(request, 'inbox/message_form.html', {'form': form, 'reply': msg, 'attachment': attachment})
        return HttpResponseRedirect('/inbox/messages/recived')


class MessageResendView(MessageFormView):
    def get(self, request, pk, *args, **kwargs):
        msg = Message.objects.get(pk=pk)
        attachment = Attachment.objects.filter(message=msg)
        form = MessageForm(request.GET)
        if msg.sender == self.request.user or self.request.user in msg.recivers.all():
            return render(request, 'inbox/message_form.html', {'form': form, 'resend': msg, 'attachment': attachment})
        return HttpResponseRedirect('/inbox/messages/recived')

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

                
            return HttpResponseRedirect('/inbox/messages/recived')

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


class InboxView(LoginRequiredMixin, TemplateView):
    template_name = 'inbox/inbox.html'


class InboxRecivedView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'inbox/recived.html'
    
    def get_queryset(self):
        page = self.request.GET.get('page')
        return Paginator(self.model.objects.filter(recivers=self.request.user), 10).get_page(page)


class InboxSentView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'inbox/sent.html'
    
    def get_queryset(self):
        page = self.request.GET.get('page')
        return Paginator(Message.objects.filter(
                sender=self.request.user, delete_for_sender=False), 10).get_page(page)


class MessageDeleteView(LoginRequiredMixin, View):
    template_name = 'inbox/inbox.html'
    
    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.recivers.remove(request.user.id)
        return redirect('/inbox/messages/recived')


class SendMessageDeleteView(LoginRequiredMixin, View):
    template_name = 'inbox/inbox.html'

    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.delete_for_sender = True
        message.save()
        return redirect('/inbox/messages/sent')