from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyProgress(request):
    user = request.user
    progress = UserProgress.objects.get(user=user)
    serializer = ProgressSerializer(progress, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)