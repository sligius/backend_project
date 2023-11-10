from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Book, FavoriteBook, Reader, Review, Critic
from .forms import ReviewForm


def create_review(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.critic = Critic.objects.get(user_id=request.user.id)
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book_id)
    else:
        initial_data = {'critic': Critic.objects.get(user_id=request.user.id), 'book': book}
        form = ReviewForm(initial=initial_data)

    return render(request, 'create_review.html',
                  {'form': form, 'book': book, 'critic': Critic.objects.get(user_id=request.user.id)})


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book=book)
    user = request.user
    user_belongs_to_critics_group = user.groups.filter(name='Critics').exists() or user.is_superuser
    return render(request, 'book_detail.html',
                  {'user_belongs_to_critics_group': user_belongs_to_critics_group, 'book': book, 'reviews': reviews})


def profile_dispatcher(request, username):
    try:
        return reader_profile(request, username)
    except Reader.DoesNotExist:
        try:
            return critic_profile(request, username)
        except Critic.DoesNotExist:
            return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@login_required
# @user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Readers').exists(), login_url='/not_access/')
def reader_profile(request, username):
    reader = Reader.objects.get(user__username=username)
    if reader.user == request.user or request.user.is_superuser:
        return render(request, 'reader_profile.html', {'reader': reader})
    else:
        return render(request, 'not_access.html')


@login_required
def critic_profile(request, username):
    critic = Critic.objects.get(user__username=username)
    if critic.user == request.user or request.user.is_superuser:
        return render(request, 'critic_profile.html', {'critic': critic})
    else:
        return render(request, 'not_access.html')


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
    if request.user.is_authenticated:
        return redirect('home/')
    else:
        if request.method == 'GET':
            return render(request, 'index.html')
        elif request.method == 'POST':
            if 'email' in request.POST:
                username = request.POST.get('create_username')
                email = request.POST.get('email')
                password = request.POST.get('create_password')
                if username and email and password:
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(username=username, email=email, password=password)
                        reader = Reader.objects.create(user=user, email=email, first_name='New', last_name='User')
                        reader.save()

                        reader_group = Group.objects.get(name='Readers')
                        reader_group.user_set.add(user)
                    else:
                        return render(request, 'login_error.html')

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

    # return render(request, 'index.html')


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
        date_of_birth = request.POST.get('date_of_birth')

        reader = Reader.objects.get(user__username=user)
        reader.first_name = first_name
        reader.last_name = last_name
        reader.date_of_birth = date_of_birth
        reader.save()

        return redirect('reader_profile', user=request.user.username)

    reader = Reader.objects.get(user__username=user)
    return render(request, 'edit_profile.html', {'reader': reader})


def home_page(request):
    return render(request, 'home_page.html')


def book_list(request):
    books = Book.objects.all()
    user_is_reader = request.user.groups.filter(name='Readers').exists()
    if request.user.is_authenticated and user_is_reader:
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            book = Book.objects.get(id=book_id)
            reader, created = Reader.objects.get_or_create(user=request.user)
            favorite, created = FavoriteBook.objects.get_or_create(reader=reader)
            favorite.book.add(book)
            return render(request, 'book_list.html', {'books': Book.objects.all()})

        else:
            for book in books:
                book.is_favourite = is_book_in_favorites(book, request.user)
            return render(request, 'book_list.html', {'books': books})
    else:
        return render(request, 'book_list.html', {'books': books,
                                                  'user_is_reader': user_is_reader})


def is_book_in_favorites(book, user):
    return FavoriteBook.objects.filter(reader__user=user, book=book).exists()


def logout_view(request):
    logout(request)
    return redirect('login')


def access_denied(request):
    return render(request, 'not_access.html')


def incorrect_login(request):
    return render(request, 'login_error.html')

# Create your views here.
