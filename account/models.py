from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):

    PLAN_CHOICES = (
        ("basic", "Cơ bản"),
        ("pro", "Chuyên nghiệp"),
    )

    plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        default="basic"
    )

    def __str__(self):
        return f"{self.username} - {self.plan}"