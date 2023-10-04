from django.shortcuts import render
from .models import Book


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)

    return render(request, 'book_detail.html', {'book': book})


# Create your views here.
