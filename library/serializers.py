from rest_framework import serializers 
from .models import Book, Loan

class BookSerializer(serializers.ModelSerializer):
    class Mata:
        model = Book
        fields = '_all_'

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '_all_'