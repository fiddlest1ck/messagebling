from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from app.models import Message
from app.forms import MessageForm


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'


class MessageView(LoginRequiredMixin, View):
    model = Message

    def get(self, request, pk, *args, **kwargs):
        try:
            instance = self.model.objects.get(pk=pk)
            if instance.sender == self.request.user or self.request.user in instance.recivers.all():
                return render(request, 'inbox/message_details.html', {'instance': instance})
            return HttpResponseRedirect('/inbox/')
        except:
            return HttpResponseRedirect('/inbox/')


class MessageFormView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.save()
            return HttpResponseRedirect('/inbox/')
        else:
            raise ValidationError('Pole {}')
    
    def get(self, request, *args, **kwargs):
        form = MessageForm(request.GET)
        return render(request, 'inbox/message_form.html', {'form': form})



class InboxView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = 'recived_messages'
    template_name = 'inbox/inbox.html'

    def get_queryset(self):
        print(self.request.user)
        return Message.objects.filter(recivers=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent_messages'] = Message.objects.filter(sender=self.request.user)
        return context