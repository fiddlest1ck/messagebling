import json

from django.contrib.auth.models import User
from django.http import JsonResponse

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
