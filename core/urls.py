from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.applications.views import (
    ProductViewSet,
    CreditApplicationViewSet,
    BankApplicationViewSet,
)

# Автоматическая генерация путей
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"applications", CreditApplicationViewSet, basename="applications")
router.register(
    r"bank/applications", BankApplicationViewSet, basename="bank-applications"
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    # OpenAPI и Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
