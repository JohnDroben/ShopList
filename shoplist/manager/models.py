from django.db import models
from django.contrib.auth.models import User

class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} (Manager)"