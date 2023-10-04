from django.db import models
from django import forms


def validate_number_length(value):
    if len(str(value)) != 4:
        raise forms.ValidationError('Год публикации должен быть четырехзначным числом')


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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор',
                               help_text='Выберите автора', null=False, blank=False)
    publication_year = models.IntegerField(validators=[validate_number_length], verbose_name='Год публикации',
                                           help_text='Введите год публикации', null=False, blank=False)
    description = models.TextField(verbose_name='Описание', help_text='Добавьте описание книги',
                                   null=False, blank=False)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f'{self.title} ({self.author.name})'

    class Meta:
        db_table = 'Book'
