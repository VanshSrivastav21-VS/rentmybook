from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books, name='books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    # path('book/<int:book_id>/view_sample/', views.view_sample, name='view_sample'),
    path('rent/<int:book_id>/', views.rent_book, name='rent_book'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('news/latest/', views.latest_news, name='latest_news'),
    path('about/', views.about, name='about'),
    path('download/<int:book_id>/', views.download_book, name='download_book'),
    path('dashboard/', views.dashboard, name='dashboard'),
]