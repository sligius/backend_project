from django.shortcuts import render
from .models import Book, FavoriteBook, Reader


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)

    return render(request, 'book_detail.html', {'book': book})


def favourite_books(request, user):
    favourite_books = FavoriteBook.objects.get()

    return render(request, 'favourite_books.html', {'favourite_books': favourite_books})


def show_index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        pass


# Create your views here.
