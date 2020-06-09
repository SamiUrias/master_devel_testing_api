from django.urls import path, re_path
from .views import Credential, Message, MessagesWithTag

urlpatterns = [
    path('credential/', Credential.as_view()),
    re_path(r'^message/(?P<id>\d+)*(/)*', Message.as_view()),
    path('messages/<str:tag>/', MessagesWithTag.as_view()),
]
