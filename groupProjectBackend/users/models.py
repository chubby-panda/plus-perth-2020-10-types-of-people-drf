from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_org = models.BooleanField(default=False)

    pass

    def __str__(self):
        return self.username
