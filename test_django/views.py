from django.shortcuts import render
from .models import Book


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)

    return render(request, 'book_detail.html', {'book': book})


def show_index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        pass


# Create your views here.
