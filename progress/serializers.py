from rest_framework import serializers
from .models import *

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = "__all__"