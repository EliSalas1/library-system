from rest_framework import serializers
from .models import Book, Loan


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, data):
        book = data['book']

        if book.available_copies <= 0:
            raise serializers.ValidationError("No hay copias disponibles de este libro.")
        
        return data
    
    def create(self, validated_data):
        book = validated_data['book']

        #redducir copia disponible
        book.available_copies -=1
        book.save()

        return super().create(validated_data)