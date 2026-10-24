import uuid
from django.db import models
from apps.users.models import Company, User
from apps.products.models import CreditProduct


class CreditApplication(models.Model):
    STATUS_CHOICES = (
        ("DRAFT", "Черновик"),
        ("PENDING", "Ожидает рассмотрения"),
        ("IN_REVIEW", "На рассмотрении"),
        ("APPROVED", "Одобрено"),
        ("REJECTED", "Отклонено"),
        ("OFFER_ACCEPTED", "Предложение принято"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="applications"
    )
    product = models.ForeignKey(CreditProduct, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    term_months = models.IntegerField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    created_at = models.DateTimeField(auto_now_add=True)


class ApplicationStatusHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        CreditApplication, on_delete=models.CASCADE, related_name="history"
    )
    status = models.CharField(max_length=20, choices=CreditApplication.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CreditDecision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.OneToOneField(
        CreditApplication, on_delete=models.CASCADE, related_name="decision"
    )
    is_approved = models.BooleanField()
    scoring_score = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    decision_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CreditOffer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    decision = models.OneToOneField(
        CreditDecision, on_delete=models.CASCADE, related_name="offer"
    )
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_term_months = models.IntegerField()
    approved_rate = models.DecimalField(max_digits=5, decimal_places=2)
    valid_until = models.DateTimeField()
