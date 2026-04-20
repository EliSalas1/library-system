from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book, Loan
from .serializers import BookSerializer, LoanSerializer
from django.utils import timezone
from datetime import timedelta


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated] #Solo usuarios

    # 🔹 DEVOLVER LIBRO
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        loan = self.get_object()

        if loan.status == 'returned':
            return Response({"error": "El libro ya fue devuelto"}, status=400)

        loan.status = 'returned'
        loan.return_date = timezone.now()
        loan.save()

        # devolver copia al inventario
        loan.book.available_copies += 1
        loan.book.save()

        return Response({"message": "Libro devuelto correctamente"})

    # 🔹 EXTENDER PRÉSTAMO
    @action(detail=True, methods=['post'])
    def extend(self, request, pk=None):
        loan = self.get_object()

        if loan.status != 'active':
            return Response({"error": "Solo préstamos activos pueden extenderse"}, status=400)

        loan.return_date = (loan.return_date or timezone.now()) + timedelta(days=7)
        loan.save()

        return Response({"message": "Préstamo extendido 7 días"})
    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # cualquiera puede ver
        return [IsAdminUser()]  #  solo admin puede crear/editar/eliminar

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author')
        year = self.request.query_params.get('year')

        if author:
            queryset = queryset.filter(author__icontains=author)

        if year:
            queryset = queryset.filter(year=year)

        return queryset

