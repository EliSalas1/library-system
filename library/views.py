from datetime import timedelta
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Loan.objects.all()

        return Loan.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()

        if loan.status == 'returned':
            return Response(
                {"error": "El préstamo ya fue devuelto completamente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pending_quantity = loan.quantity - loan.returned_quantity

        if pending_quantity <= 0:
            return Response(
                {"error": "No hay copias pendientes por devolver."},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.returned_quantity += pending_quantity
        loan.return_date = timezone.now()
        loan.update_status()
        loan.save()

        loan.book.available_copies += pending_quantity
        loan.book.save()

        return Response({
            "message": "Libro devuelto completamente.",
            "status": loan.status,
            "returned_quantity": loan.returned_quantity
        })

    @action(detail=True, methods=['post'])
    def partial_return(self, request, pk=None):
        loan = self.get_object()
        quantity_to_return = request.data.get('quantity')

        if loan.status == 'returned':
            return Response(
                {"error": "El préstamo ya fue devuelto completamente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity_to_return is None:
            return Response(
                {"error": "Debes enviar la cantidad a devolver."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantity_to_return = int(quantity_to_return)
        except (TypeError, ValueError):
            return Response(
                {"error": "La cantidad debe ser un número entero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity_to_return <= 0:
            return Response(
                {"error": "La cantidad debe ser mayor a 0."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pending_quantity = loan.quantity - loan.returned_quantity

        if quantity_to_return > pending_quantity:
            return Response(
                {"error": f"No puedes devolver más de lo pendiente ({pending_quantity})."},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.returned_quantity += quantity_to_return
        if loan.returned_quantity == loan.quantity:
            loan.return_date = timezone.now()

        loan.update_status()
        loan.save()

        loan.book.available_copies += quantity_to_return
        loan.book.save()

        return Response({
            "message": "Devolución parcial registrada correctamente.",
            "status": loan.status,
            "returned_quantity": loan.returned_quantity,
            "pending_quantity": loan.quantity - loan.returned_quantity
        })

    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        loan = self.get_object()

        if loan.status == 'returned':
            return Response(
                {"error": "No se puede extender un préstamo ya devuelto."},
                status=status.HTTP_400_BAD_REQUEST
            )

        loan.due_date = (loan.due_date or timezone.now()) + timedelta(days=7)
        loan.save()

        return Response({
            "message": "Préstamo extendido 7 días.",
            "due_date": loan.due_date
        })


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')

        if author:
            queryset = queryset.filter(author__icontains=author)

        if year:
            queryset = queryset.filter(year=year)

        return queryset