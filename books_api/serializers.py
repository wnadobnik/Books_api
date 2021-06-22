from rest_framework import serializers
from books_api.models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

# Serializers define the API representation.
class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True)
    class Meta:
        model = Book
        fields = ['title', 'authors', 'published_date', 'categories',
                  'average_rating', 'ratings_count', 'thumbnail']