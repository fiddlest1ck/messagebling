"""messagebling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app.utils import serve_users
from app.views import (HomeView, InboxView, MessageView, MessageFormView,
                       MessageReplyView, MessageResendView, UploadAttachmentView,
                       MessageDeleteView, SendMessageDeleteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('api/users/', serve_users, name='serveusers'),
    path('api/attachments/', UploadAttachmentView.as_view(), name='attachments'),
    path('inbox/messages/', MessageFormView.as_view(), name='messageform'),
    path('inbox/messages/<int:pk>' , MessageView.as_view(), name='message'),
    path('inbox/messages/<int:pk>/reply', MessageReplyView.as_view(), name='messagereply'),
    path('inbox/messages/<int:pk>/resend', MessageResendView.as_view(), name='messageresend'),
    path('inbox/message/<int:pk>/delete', MessageDeleteView.as_view(), name='messagedelete'),
    path('inbox/message/<int:pk>/senderdelete', SendMessageDeleteView.as_view(), name='messagesenderdelete'),
    path('', HomeView.as_view(), name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

