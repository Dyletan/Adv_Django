from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer
from products.models import Product

class CreateBuyOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.role not in ["customer", "trader", "admin"]:
            return Response({"error": "Only customers or traders can place buy orders."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['user'] = request.user.id
        data['product'] = product.id
        data['order_type'] = 'buy'
        data['status'] = 'pending'

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            buy_order = serializer.save()

            sell_order = Order.objects.create(
                user=product.seller,
                product=product,
                order_type='sell',
                quantity=buy_order.quantity,
                price=buy_order.price,
                status='pending'
            )

            transaction = Transaction.objects.create(
                buy_order=buy_order,
                sell_order=sell_order,
                quantity=buy_order.quantity,
                price=buy_order.price,
                payment_status='pending'
            )

            return Response({
                "message": "Buy order placed successfully. Sell order and transaction created for review.",
                "buy_order": OrderSerializer(buy_order).data,
                "sell_order": OrderSerializer(sell_order).data,
                "transaction": TransactionSerializer(transaction).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        if request.user.role != "sales_rep":
            return Response({"error": "Only sales representatives can approve transactions."}, status=status.HTTP_403_FORBIDDEN)

        transaction = get_object_or_404(Transaction, id=transaction_id)

        if transaction.payment_status != 'pending':
            return Response({"error": "Transaction is already processed."}, status=status.HTTP_400_BAD_REQUEST)

        transaction.payment_status = 'approved'
        transaction.save()

        return Response({"message": "Transaction approved.", "transaction": TransactionSerializer(transaction).data})

class CancelTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        if request.user.role != "sales_rep":
            return Response({"error": "Only sales representatives can cancel transactions."}, status=status.HTTP_403_FORBIDDEN)

        transaction = get_object_or_404(Transaction, id=transaction_id)

        if transaction.payment_status != 'pending':
            return Response({"error": "Only pending transactions can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        transaction.payment_status = 'rejected'
        transaction.buy_order.status = 'cancelled'
        transaction.sell_order.status = 'cancelled'
        transaction.buy_order.save()
        transaction.sell_order.save()
        transaction.save()

        return Response({"message": "Transaction cancelled.", "transaction": TransactionSerializer(transaction).data})

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from trading.models import Transaction
from trading.serializers import TransactionSerializer

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Transaction.objects.all()
        if self.request.user.role == "sales_rep":
            return qs.filter(payment_status='pending')
        return qs.filter(buy_order__user=self.request.user) | qs.filter(sell_order__user=self.request.user)

