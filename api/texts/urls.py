from django.urls import path
from .views import Credential

urlpatterns = [
    path('credential/', Credential.as_view()),
]
