from django.urls import path
from .views import Credential, Message

urlpatterns = [
    path('credential/', Credential.as_view()),
    path('message/', Message.as_view()),
]
