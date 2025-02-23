from django.db import models
from django.contrib.auth import get_user_model
from challenges.models import Challenge
 
User = get_user_model() 
 
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('started', 'Started'),
                ('submitted', 'Submitted'),
                ('completed', 'Completed')]
    )
    attempts = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"
    
# User Submissions Model
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    code = models.TextField()
    output = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.challenge.title}"

# Discussion Forum Model
class Discussion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discussion: {self.title} by {self.user.username}"








