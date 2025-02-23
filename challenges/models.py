from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Challenge(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    test_cases = models.JSONField(default=list) 
    difficulty = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'),
                ('intermediate', 'Intermediate'),
                ('advanced', 'Advanced')]
    )
    points = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# User Achievements Model
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

