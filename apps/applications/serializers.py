from rest_framework import serializers
from .models import CreditApplication, ApplicationStatusHistory, CreditOffer
from apps.products.models import CreditProduct
from apps.repayment.models import RepaymentScenario


class CreditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditProduct
        fields = "__all__"


class CreditApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditApplication
        fields = "__all__"


class ApplicationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatusHistory
        fields = "__all__"


class CreditOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditOffer
        fields = "__all__"


class RepaymentScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepaymentScenario
        fields = "__all__"
