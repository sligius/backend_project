"""
URL configuration for FirstLabBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from test_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('favourite_books/<str:user>/', views.favourite_books, name='favourite_books'),
    path('books/', views.book_list, name='books'),
    re_path(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile_dispatcher, name='profile_dispatcher'),
    path('', views.show_index, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='home'),
    path('new_review/<int:book_id>/', views.create_review, name='create_review'),
    path('edit_profile/<str:user>/', views.edit_profile, name='edit_profile'),
    path('not_access/', views.access_denied, name='not_access'),
    path('incorrect_login/', views.incorrect_login, name='login_error'),
    path('request/', views.request_form, name='request_form'),
    path('validate_username', views.validate_username, name='validate_username'),
    path('update_heart_icon/', views.update_heart_icon, name='update_heart_icon'),
]
