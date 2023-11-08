import datetime

from django.contrib.auth.models import User
from django.db import models
from django import forms


def validate_number_length(value):
    if len(str(value)) != 4:
        raise forms.ValidationError('Год публикации должен быть четырехзначным числом')


class Reader(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id читателя",
                             help_text="Выберите id читателя", null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Введите имя", null=False, blank=False)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", help_text="Введите фамилию",
                                 null=True, blank=True)
    email = models.EmailField(verbose_name='Email')
    date_of_birth = models.DateField(verbose_name='Дата рождения', blank=True, null=True, default=datetime.date.today)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Reader'


class Critic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='id критика',
                             help_text="Выберите id критика", null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя', help_text='Введите имя', null=False, blank=False)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', help_text='Введите фамилию',
                                 null=True, blank=True)
    email = models.EmailField(verbose_name='Email')
    organization = models.CharField(max_length=200, verbose_name='Организация', blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(verbose_name='Стаж работы', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Critic'


class Author(models.Model):
    name = models.CharField(max_length=100, primary_key=True, verbose_name='Имя',
                            help_text='Введите имя автора', null=False, blank=False)
    language = models.CharField(max_length=100, verbose_name='Язык',
                                help_text='Введите язык, который использует автор для своих книг',
                                null=True, blank=True)
    birth_date = models.DateField()
    biography = models.TextField(verbose_name='Об авторе', help_text='Расскажите немного о жизни автора',
                                 null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Author'


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название',
                            help_text='Введите название жанра', null=False, blank=False)
    description = models.TextField(verbose_name='Описание', help_text='Добавьте описание жанра',
                                   null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Genre'


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название',
                             help_text='Введите название книги', null=False, blank=False)
    author = models.ManyToManyField(Author, verbose_name='Автор', help_text='Выберите автора', blank=False)
    publication_year = models.IntegerField(validators=[validate_number_length], verbose_name='Год публикации',
                                           help_text='Введите год публикации', null=False, blank=False)
    description = models.TextField(verbose_name='Описание', help_text='Добавьте описание книги',
                                   null=False, blank=False)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        author_names = ", ".join([author.name for author in self.author.all()])
        return f'{self.title} ({author_names})'

    class Meta:
        db_table = 'Book'


class Review(models.Model):
    critic = models.ForeignKey(Critic, on_delete=models.CASCADE, verbose_name='Критик',help_text="Выберите критика",
                               null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга', help_text="Выберите книгу",
                             null=False, blank=False)
    content = models.TextField(verbose_name='Рецензия', help_text="Напишите Вашу рецензию", null=False, blank=False)

    def __str__(self):
        return f'Рецензия от критика {self.critic.user.username} на книгу "{self.book.title}"'

    class Meta:
        db_table = 'Review'


class FavoriteBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="id читателя",
                               help_text="Выберите читателя", null=True, blank=True)
    book = models.ManyToManyField(Book, help_text="Выберите книги")

    def __str__(self):
        return f'Любимые книги читателя {self.reader}'

    class Meta:
        db_table = 'Favourite Book'