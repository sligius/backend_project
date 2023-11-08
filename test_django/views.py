from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
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
    elif request.method == 'POST':
        if 'email' in request.POST:
            print('registration')
            username = request.POST.get('create_username')
            email = request.POST.get('email')
            password = request.POST.get('create_password')
            if username and email and password:
                user = User.objects.create_user(username=username, email=email, password=password)
                reader = Reader.objects.create(user=user, email=email, first_name='New', last_name='User')
                reader.save()

            login(request, user)
            return redirect('home/')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            try:
                login(request, user)
                return redirect('home/')
            except:
                return redirect('login')

    #return render(request, 'index.html')

'''
@login_required
def edit_profile(request):
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        try:
            reader = Reader.objects.get(user=request.user)
            reader.first_name = first_name
            reader.last_name = last_name
            reader.save()

            return HttpResponse('Профиль успешно обновлен')
        except Reader.DoesNotExist:
            return HttpResponse('Профиль не найден')
    else:
        return HttpResponse('Метод не поддерживается')
'''


@login_required
def edit_profile(request, user):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        reader = Reader.objects.get(user__username=user)
        reader.first_name = first_name
        reader.last_name = last_name
        reader.save()

        return redirect('reader_profile', user=request.user.username)

    reader = Reader.objects.get(user__username=user)
    return render(request, 'edit_profile.html', {'reader': reader})


def home_page(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'home_page.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
# Create your views here.
