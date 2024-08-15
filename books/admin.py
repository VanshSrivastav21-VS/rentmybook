from django.contrib import admin
from .models import Book, Rental, Purchase

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    search_fields = ('title', 'author')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rental_date', 'return_date')
    list_filter = ('rental_date', 'return_date')
    search_fields = ('user__username', 'book__title')

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('user__username', 'book__title')