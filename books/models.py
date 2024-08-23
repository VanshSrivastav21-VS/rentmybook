from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    sample_pdf = models.FileField(upload_to='book_samples/')
    full_pdf = models.FileField(upload_to='book_full/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)
    
    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
class News(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='news_images/')
    
    class Meta:
        verbose_name_plural = "News"
        
    def __str__(self):
        return self.title