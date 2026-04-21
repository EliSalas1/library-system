from rest_framework import serializers
from .models import Book, Loan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_year(self, value):
        if value < 0:
            raise serializers.ValidationError("El año no puede ser negativo")
        return value

    def validate(self, data):
        available = data.get('available_copies')
        total = data.get('total_copies')

        if available is not None and total is not None and available > total:
            raise serializers.ValidationError(
                "Las copias disponibles no pueden ser mayores al total."
            )
        return data

    def validate_image(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("La imagen no debe superar 2MB")

            if not value.content_type.startswith('image'):
                raise serializers.ValidationError("El archivo debe ser una imagen")

        return value


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ['user', 'returned_quantity', 'status', 'return_date']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0.")
        return value

    def validate(self, data):
        book = data['book']
        quantity = data.get('quantity', 1)

        if book.available_copies < quantity:
            raise serializers.ValidationError(
                f"No hay suficientes copias disponibles. Disponibles: {book.available_copies}."
            )

        return data

    def create(self, validated_data):
        book = validated_data['book']
        quantity = validated_data.get('quantity', 1)

        book.available_copies -= quantity
        book.save()

        loan = Loan.objects.create(**validated_data)
        loan.update_status()
        loan.save()

        return loan