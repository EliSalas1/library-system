from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('partial', 'Partial'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    returned_quantity = models.PositiveIntegerField(default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def update_status(self):
        if self.returned_quantity == 0:
            self.status = 'active'
        elif self.returned_quantity < self.quantity:
            self.status = 'partial'
        else:
            self.status = 'returned'

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"