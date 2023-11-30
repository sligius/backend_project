from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from .models import Book, FavoriteBook, Reader, Review, Critic
from .forms import ReviewForm, RequestForm


def create_review(request, book_id):
    """
        Создание отзыва на книгу. Обрабатывается как GET, так и POST запросы.
        При GET запросе отображается форма для создания отзыва.
        При POST запросе проверяются данные формы и создается новый отзыв.
        Доступно только для группы критиков.
    """
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
    """
        Отображение деталей книги, включая все отзывы на книгу.
        Также проверяется, принадлежит ли текущий пользователь к группе критиков или является суперпользователем.
        Если проверка пройдена, то предоставляется функция добавления отзыва к книге.
        Критик также может удалять свои отзывы к книге.
    """
    book = Book.objects.get(pk=book_id)
    reviews = Review.objects.filter(book=book)
    user = request.user
    user_belongs_to_critics_group = user.groups.filter(name='Critics').exists() or user.is_superuser
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review = Review.objects.get(id=review_id)
        if review.critic.user == user and user_belongs_to_critics_group:
            review.delete()
            return redirect('book_detail', book_id=book_id)

    return render(request, 'book_detail.html',
                  {'user': user, 'user_belongs_to_critics_group': user_belongs_to_critics_group,
                   'book': book, 'reviews': reviews})


def profile_dispatcher(request, username):
    """
        Действует как диспетчер, направляя запрос либо к методу reader_profile, либо к методу critic_profile.
        Если ни Reader, ни Critic не существуют с указанным именем пользователя, возвращает ошибку 404.
    """
    try:
        return reader_profile(request, username)
    except Reader.DoesNotExist:
        try:
            return critic_profile(request, username)
        except Critic.DoesNotExist:
            return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@login_required
def reader_profile(request, username):
    """
        Отображение профиля читателя. Доступ к этому представлению имеют только сам читатель или суперпользователь.
    """
    reader = Reader.objects.get(user__username=username)
    if reader.user == request.user or request.user.is_superuser:
        return render(request, 'reader_profile.html', {'reader': reader})
    else:
        return render(request, 'not_access.html')


@login_required
def critic_profile(request, username):
    """
        Отображение профиля критика. Доступ к этому представлению имеют только сам критик или суперпользователь.
    """
    critic = Critic.objects.get(user__username=username)
    if critic.user == request.user or request.user.is_superuser:
        return render(request, 'critic_profile.html', {'critic': critic})
    else:
        return render(request, 'not_access.html')


def favourite_books(request, user):
    """
        Отображение списка любимых книг конкретного читателя.
        Также обрабатываются POST-запросы для удаления книги из избранного.
    """
    user_object = User.objects.get(username=user)
    reader = Reader.objects.get(user_id=user_object.id)
    favourite_books = FavoriteBook.objects.filter(reader=reader)
    current_user = request.user
    if current_user.is_authenticated:
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            book = Book.objects.get(id=book_id)
            favourite_book = FavoriteBook.objects.get(reader=reader)
            favourite_book.book.remove(book)
        return render(request, 'favourite_books.html', {'favourite_books': favourite_books})
    else:
        return render(request, 'not_access.html')


def show_index(request):
    """
        Отображение главной страницы. Если пользователь аутентифицирован, происходит перенаправление
        на домашнюю страницу.
        Также обрабатываются POST-запросы для создания нового пользователя или входа в систему
        существующего пользователя.
    """
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


def validate_username(request):
    """
        Проверка доступности логина
    """
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


@login_required
def edit_profile(request, user):
    """
        Редактирование профиля читателя. Обрабатываются как GET, так и POST запросы.
        При GET запросе отображается форма для редактирования профиля.
        При POST запросе проверяются данные формы и обновляется профиль читателя.
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')

        reader = Reader.objects.get(user__username=user)
        reader.first_name = first_name
        reader.last_name = last_name
        reader.date_of_birth = date_of_birth
        reader.save()

        return redirect('profile_dispatcher', username=request.user.username)

    reader = Reader.objects.get(user__username=user)
    return render(request, 'edit_profile.html', {'reader': reader})


def home_page(request):
    """
        Отображение домашней страницы.
    """
    return render(request, 'home_page.html')


def book_list(request):
    """
        Отображение списка всех книг. Если пользователь аутентифицирован и является читателем,
        также есть возможность добавлять или удалять книги из избранного.
    """
    books = Book.objects.all()
    user_is_reader = request.user.groups.filter(name='Readers').exists()
    print(user_is_reader)
    if request.user.is_authenticated and user_is_reader:
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            book = Book.objects.get(id=book_id)
            reader, created = Reader.objects.get_or_create(user=request.user)
            favorite, created = FavoriteBook.objects.get_or_create(reader=reader)
            if is_book_in_favorites(book, request.user):
                favorite.book.remove(book)
            else:
                favorite.book.add(book)
            return render(request, 'book_list.html', {'books': Book.objects.all(),
                                                      'user_is_reader': user_is_reader})

        else:
            for book in books:
                book.is_favourite = is_book_in_favorites(book, request.user)
            return render(request, 'book_list.html', {'books': books, 'user_is_reader': user_is_reader})
    else:
        return render(request, 'book_list.html', {'books': books,
                                                  'user_is_reader': user_is_reader})


def is_book_in_favorites(book, user):
    """
        Проверка, находится ли книга в избранном у пользователя.
    """
    return FavoriteBook.objects.filter(reader__user=user, book=book).exists()


def logout_view(request):
    """
        Выход из системы пользователя и перенаправление его на страницу входа.
    """
    logout(request)
    return redirect('login')


def access_denied(request):
    """
        Отображение страницы, информирующей пользователя о том, что у него нет доступа к запрашиваемому ресурсу.
    """
    return render(request, 'not_access.html')


def incorrect_login(request):
    """
        Отображение страницы, информирующей пользователя о том, что его попытка входа в систему была неудачной.
    """
    return render(request, 'login_error.html')


def request_form(request):
    """
        Создание заявки на добавление автора/книги на сайт.
        Обрабатывается как GET, так и POST запросы.
        При GET запросе отображается форма для создания заявки.
        При POST запросе проверяются данные формы и создается новая заявка.
        Доступно для всех пользователей.
    """
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'home_page.html')
    else:
        form = RequestForm()

    return render(request, 'request_form.html', {'form': form})