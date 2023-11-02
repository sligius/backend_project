from django.contrib import admin

from test_django.models import *

admin.site.register(Author)
admin.site.register(Reader)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(FavoriteBook)
admin.site.register(Review)
admin.site.register(Critic)

