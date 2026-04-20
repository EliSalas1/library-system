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
    
    def validate(self,data):
        if data['available_copies'] > data['total_copies']:
            raise serializers.ValidationError(
                "Las copias disponobles no pueden ser mayores al total"
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

    def validate(self, data):
        book = data['book']

        if book.available_copies <= 0:
            raise serializers.ValidationError(
                "No hay copias disponibles de este libro."
            )
        
        return data
    
    def create(self, validated_data):
        book = validated_data['book']

        #redducir copia disponible
        book.available_copies -=1
        book.save()

        return super().create(validated_data)