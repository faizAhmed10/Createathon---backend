from django.urls import path
from .views import *

urlpatterns = [
    path('', challengeViewSet, name="challenges"),
    path('verify_solution/<int:challenge_id>/', verify_solution, name="challenge-verification"),
    path('<int:id>/', getChallenge, name="getChallenge")
]
