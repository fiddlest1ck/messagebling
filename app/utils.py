import json

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout
from app.models import Notification, Message
from django.http import JsonResponse
from django.shortcuts import redirect

def serve_users(request):
    if request.is_ajax():
        q = request.GET.get('q', '')
        users = User.objects.filter(username__contains=q).values("pk", 'username')
        users = list(users)
        print(users)
        return JsonResponse(users, safe=False)
    else:
        return JsonResponse(data={'success': False,
                                  'errors': 'Nie znaleziono wyników'})

def logout_view(request):
    logout(request)
    return redirect('/')

def count_notifications(request):
    data_dict = {'notifications': list()}
    notifications = Notification.objects.filter(Q(users=request.user) & ~Q(readed_by=request.user))
    if request.is_ajax():
        data_dict['notifications'].append(list(notifications.values('message_id', 'id')))
        data_dict['message_count'] = Message.objects.filter(Q(recivers=request.user) & ~Q(readed_by=request.user)).count()
        data_dict['count'] = notifications.count()
        return JsonResponse(data_dict, safe=False)


def delete_notifications(request, pk):
    if request.is_ajax() and request.POST:
        notification = Notification.objects.get(pk=pk)
        notification.readed_by.add(request.user)
        notification.save()
