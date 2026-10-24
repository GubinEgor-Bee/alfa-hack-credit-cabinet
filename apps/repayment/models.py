import uuid
from django.db import models
from apps.applications.models import CreditApplication


class RepaymentScenario(models.Model):
    SCENARIO_TYPES = (
        ("REDUCE_PAYMENT", "Уменьшение платежа"),
        ("REDUCE_TERM", "Уменьшение срока"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(
        CreditApplication, on_delete=models.CASCADE, related_name="repayment_scenarios"
    )
    early_repayment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    scenario_type = models.CharField(max_length=20, choices=SCENARIO_TYPES)
    new_monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)
    new_term_months = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
