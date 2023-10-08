# Generated by Django 4.2.5 on 2023-10-08 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_django', '0002_alter_author_biography_remove_book_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Critic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите имя', max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, help_text='Введите фамилию', max_length=100, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('user', models.ForeignKey(blank=True, help_text='Выберите id критика', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id критика')),
            ],
            options={
                'db_table': 'Critic',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='Напишите Вашу рецензию', verbose_name='Рецензия')),
                ('book', models.ForeignKey(help_text='Выберите книгу', on_delete=django.db.models.deletion.CASCADE, to='test_django.book', verbose_name='Книга')),
                ('critic', models.ForeignKey(help_text='Выберите критика', on_delete=django.db.models.deletion.CASCADE, to='test_django.critic', verbose_name='Критик')),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите имя', max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, help_text='Введите фамилию', max_length=100, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('user', models.ForeignKey(blank=True, help_text='Выберите id читателя', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='id читателя')),
            ],
            options={
                'db_table': 'Reader',
            },
        ),
        migrations.CreateModel(
            name='FavoriteBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(blank=True, help_text='Выберите id книги', null=True, on_delete=django.db.models.deletion.CASCADE, to='test_django.book', verbose_name='id книги')),
                ('reader', models.ForeignKey(blank=True, help_text='Выберите id читателя', null=True, on_delete=django.db.models.deletion.CASCADE, to='test_django.reader', verbose_name='id читателя')),
            ],
            options={
                'db_table': 'Favourite Book',
            },
        ),
    ]
