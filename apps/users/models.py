import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLE_CHOICES = (
        ("CLIENT", "Клиент"),
        ("BANK_OPERATOR", "Сотрудник банка"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CLIENT")


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    inn = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    BUSINESS_TYPE_CHOICES = (
        ("IP", "ИП"),
        ("OOO", "ООО"),
    )
    business_type = models.CharField(max_length=10, choices=BUSINESS_TYPE_CHOICES)
