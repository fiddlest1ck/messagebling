import json

from django.contrib.auth.models import User
from django.http import HttpResponse

def serve_users(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__contains=q)
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username
            results.append(user_json)
        print(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)