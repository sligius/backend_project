from django.contrib import admin

from test_django.models import *

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)

