from django.urls import path
from .views import UserCreateView, PaymentListView, CreatePaymentView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-payment/', CreatePaymentView.as_view(), name='create-payment'),
]
