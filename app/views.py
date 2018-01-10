from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from app.models import Message


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'


class InboxView(LoginRequiredMixin, ListView):
    model = Message