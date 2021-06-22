from django.urls import path, include
from books_api.views import BookViewSet, BookView
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.

urlpatterns = [
    path('books/<int:id>', BookView.as_view()),
    path(r'books', BookViewSet.as_view())
]
