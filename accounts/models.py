from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    # Additional fields
    points = models.IntegerField(default=0)  # Points for completing challenges
    challenges_completed = models.IntegerField(default=0)  # Number of completed challenges
    achievements = models.TextField(blank=True, null=True)  # Store achievements as JSON or comma-separated values

    LEVELS = [
        ("Novice", "Novice"),
        ("Intermediate", "Intermediate"),
        ("Veteran", "Veteran"),
        ("Expert", "Expert"),
    ]
    level = models.CharField(max_length=20, choices=LEVELS, default="Novice")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def update_level(self):
        """Updates user level based on points."""
        if self.points < 100:
            self.level = "Novice"
        elif 100 <= self.points < 500:
            self.level = "Intermediate"
        elif 500 <= self.points < 1000:
            self.level = "Veteran"
        else:
            self.level = "Expert"
        self.save()

    def add_points(self, points):
        """Adds points to the user and updates their level."""
        self.points += points
        self.challenges_completed += 1
        self.update_level()
        self.save()
    
 