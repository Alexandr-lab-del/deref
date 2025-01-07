from django.urls import path
from .views import UserCreateView, PaymentListView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]
