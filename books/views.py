from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .forms import RentBookForm
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
        form = RentBookForm(request.POST)
        if form.is_valid():
            # Handle form data, e.g., save rental details to the database
            
            # Proceed to payment
            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': book.title,
                            },
                            'unit_amount': int(book.rental_price * 100),  # amount in cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(session.url, code=303)

    else:
        form = RentBookForm()
    
    return render(request, 'books/rent_book.html', {'form': form, 'book': book})

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
    return render(request, 'books/dashboard.html', {'rentals': rentals, 'purchases': purchases})

def latest_news(request):
    news_items = News.objects.order_by('-date')    # [:3]
    return render(request, 'books/latest_news.html', {'news_items': news_items})

def about(request):
    return render(request, 'books/about.html')

