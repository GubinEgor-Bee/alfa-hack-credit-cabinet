from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import CreditApplication, ApplicationStatusHistory, CreditOffer
from .serializers import (
    CreditApplicationSerializer,
    ApplicationHistorySerializer,
    CreditOfferSerializer,
    RepaymentScenarioSerializer,
    CreditProductSerializer,
)
from apps.products.models import CreditProduct


# 1. Продукты
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/products/"""

    queryset = CreditProduct.objects.all()
    serializer_class = CreditProductSerializer


# 2. Клиентская часть (Заявки)
class CreditApplicationViewSet(viewsets.ModelViewSet):
    """POST, PATCH, GET /api/v1/applications/"""

    queryset = CreditApplication.objects.all()
    serializer_class = CreditApplicationSerializer

    @extend_schema(responses={200: dict})
    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Отправка заявки на рассмотрение в банк"""
        return Response({"status": "PENDING"})

    @extend_schema(responses={200: ApplicationHistorySerializer(many=True)})
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        """Получение истории статусов заявки"""
        return Response([])

    @extend_schema(responses={200: CreditOfferSerializer})
    @action(detail=True, methods=["get"])
    def offer(self, request, pk=None):
        """Получение индивидуального кредитного предложения"""
        return Response({"approved_amount": 800000, "approved_rate": 16.5})

    @extend_schema(responses={200: RepaymentScenarioSerializer(many=True)})
    @action(detail=True, methods=["get", "post"], url_path="repayment-scenarios")
    def repayment_scenarios(self, request, pk=None):
        """Конструктор досрочного погашения (создание и просмотр)"""
        if request.method == "POST":
            return Response(
                {
                    "early_repayment_amount": request.data.get(
                        "early_repayment_amount"
                    ),
                    "new_monthly_payment": 15000,
                    "new_term_months": 10,
                }
            )
        return Response([])


# 3. Банковская часть (РМ Оператора)
class BankApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/v1/bank/applications/"""

    queryset = CreditApplication.objects.filter(status="PENDING")
    serializer_class = CreditApplicationSerializer

    @extend_schema(responses={200: dict})
    @action(detail=True, methods=["post"])
    def decision(self, request, pk=None):
        """Запуск логики скоринга (Егор Б.) и фиксация решения"""
        return Response(
            {"is_approved": True, "scoring_score": 750, "status": "APPROVED"}
        )
