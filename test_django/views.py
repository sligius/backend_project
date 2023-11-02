from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Book, FavoriteBook, Reader


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)

    return render(request, 'book_detail.html', {'book': book})


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
