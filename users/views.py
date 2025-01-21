from rest_framework import generics, status
from .models import User, Payment, Product
from .serializers import UserSerializer, PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import create_product, create_price, create_checkout_session


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['date']
    permission_classes = [IsAuthenticated]


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        amount = request.data.get("amount")
        method = request.data.get("method", "stripe")

        if not product_id or not amount:
            return Response({"error": "Product ID and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)

            stripe_product = create_product(name=product.name)
            stripe_price = create_price(product_id=stripe_product["id"], amount=int(float(amount)))

            success_url = "http://127.0.0.1:8000/success/"
            cancel_url = "http://127.0.0.1:8000/cancel/"
            session = create_checkout_session(
                price_id=stripe_price["id"],
                success_url=success_url,
                cancel_url=cancel_url,
            )

            payment = Payment.objects.create(
                user=user,
                product=product,
                amount=amount,
                method=method,
                stripe_session_id=session["id"],
                payment_url=session["url"],
            )

            return Response(
                {
                    "payment_url": session["url"],
                },
                status=status.HTTP_201_CREATED,
            )
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
