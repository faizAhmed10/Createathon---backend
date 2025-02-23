from django.urls import path
from .views import *

urlpatterns = [
    path('user-progress/', getMyProgress, name="get-progress")
]
