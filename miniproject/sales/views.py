from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import SalesOrder, Invoice
from .serializers import SalesOrderSerializer, InvoiceSerializer
from trading.models import Transaction

class SalesOrderListView(generics.ListAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SalesOrder.objects.all()

class CreateSalesOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id, payment_status='approved')
        final_price = transaction.price * transaction.quantity
        sales_order = SalesOrder.objects.create(transaction=transaction, final_price=final_price)
        return Response({
            "message": "SalesOrder created.",
            "sales_order": SalesOrderSerializer(sales_order).data
        }, status=status.HTTP_201_CREATED)

class GenerateInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, sales_order_id):
        sales_order = get_object_or_404(SalesOrder, id=sales_order_id)
        due_date = request.data.get("due_date", "2025-12-31")
        invoice = Invoice.objects.create(sales_order=sales_order, due_date=due_date)
        return Response({
            "message": "Invoice generated.",
            "invoice": InvoiceSerializer(invoice).data
        }, status=status.HTTP_201_CREATED)

class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.all()

class PayInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        if invoice.is_paid:
            return Response({"error": "Invoice already paid."}, status=status.HTTP_400_BAD_REQUEST)
        
        invoice.is_paid = True
        invoice.save()
        
        sales_order = invoice.sales_order
        sales_order.status = "paid"
        sales_order.save()
        
        transaction = sales_order.transaction
        order = transaction.buy_order
        product = order.product

        product.quantity = max(product.quantity - order.quantity, 0)
        product.save()
        
        return Response({
            "message": "Invoice paid successfully. SalesOrder status updated to paid and product quantity reduced.",
            "invoice": InvoiceSerializer(invoice).data
        }, status=status.HTTP_200_OK)