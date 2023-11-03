from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Book, FavoriteBook, Reader, Review
from .forms import ReviewForm


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            return redirect('book_detail', book_id=review.book.id)
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form})


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


def reader_profile(request, user):
    reader = Reader.objects.get(user__username=user)
    return render(request, 'reader_profile.html', {'reader': reader})


def favourite_books(request, user):
    user_object = User.objects.get(username=user)
    reader = Reader.objects.get(user_id=user_object.id)
    favourite_books = FavoriteBook.objects.filter(reader=reader)
    current_user = request.user
    if current_user.is_authenticated:
        return render(request, 'favourite_books.html', {'favourite_books': favourite_books})
    else:
        return render(request, 'not_access.html')


def show_index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        pass

# Create your views here.
