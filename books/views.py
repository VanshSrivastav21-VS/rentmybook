from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import RentBookForm
from django.http import JsonResponse
from .models import Book, Rental, Purchase, News
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

def home(request):
    books = Book.objects.all().order_by('-id')[:4]
    news_items = News.objects.order_by('-date')[:3]
    return render(request, 'books/home.html', {'books': books, 'news_items':news_items})


def books(request):
    books = Book.objects.all().order_by('-id')
    return render(request, 'books/books.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def rent_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        # Get the Stripe token submitted by the form
        token = request.POST.get('stripeToken')

        try:
            # Create a Stripe charge
            charge = stripe.Charge.create(
                amount=int(book.price * 100),  # Amount in cents
                currency='usd',
                description=f'Rental payment for {book.title}',
                source=token,
            )

            # If charge is successful, create a Rental record
            Rental.objects.create(
                user=request.user,
                book=book,
                return_date=calculate_return_date(),  # You need to implement this
            )

            # Redirect to a success page or the user's dashboard
            return redirect('dashboard')

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            return JsonResponse({'error': str(e)}, status=400)

    context = {
        'book': book,
    }
    return render(request, 'books/rent_book.html', context)

def calculate_return_date():
    from datetime import datetime, timedelta
    # Assuming a rental period of 14 days
    return datetime.now() + timedelta(days=3)

@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(book.price * 100),  # Amount in cents
                currency='usd',
                source=token,
                description=f'Purchase of {book.title}'
            )
            Purchase.objects.create(user=request.user, book=book)
            return redirect('download_book', book_id=book.id)
        except stripe.error.CardError as e:
            # Handle card error
            error_message = str(e)
            return render(request, 'books/buy_book.html', {'book': book, 'error_message': error_message})

    return render(request, 'books/buy_book.html', {'book': book})

@login_required
def download_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    # Logic to serve the PDF file
    return redirect('dashboard')

@login_required
def dashboard(request):
    rentals = Rental.objects.filter(user=request.user)
    purchases = Purchase.objects.filter(user=request.user)
    now = timezone.now()

    for rental in rentals:
        remaining_time = rental.return_date - now
        rental.remaining_days = remaining_time.days
        rental.remaining_hours = remaining_time.seconds // 3600
        rental.remaining_minutes = (remaining_time.seconds % 3600) // 60
        rental.remaining_seconds = (remaining_time.seconds % 3600) % 60

    return render(request, 'books/dashboard.html', {'rentals': rentals, 'purchases': purchases, 'now': now})

def latest_news(request):
    news_items = News.objects.order_by('-date')    # [:3]
    return render(request, 'books/latest_news.html', {'news_items': news_items})

def about(request):
    return render(request, 'books/about.html')



