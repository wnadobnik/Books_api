from books_api.serializers import BookSerializer
from books_api.models import Book
from rest_framework import generics, status
import requests
from rest_framework.response import Response

class BookViewSet(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        result = Book.objects.all()
        published_date = self.request.query_params.get('published_date')
        authors = self.request.query_params.getlist('author', '')
        sort = self.request.query_params.get('sort')
        if published_date:
            if isinstance(published_date, int) and len(published_date) <= 4:
                result = result.filter(published_date=published_date)
        if authors:
            result = result.filter(authors__name=authors)
        if sort == '-published_date' or sort == "published_date":
            result = result.order_by(sort)
        return result.distinct()

    def post(self, request):
        q = request.query_params.get('q')
        url = f'https://www.googleapis.com/books/v1/volumes?q={q}'
        r = requests.get(url)
        books = r.json()['items']
        for book in books:
            title = book['volumeInfo']['title']
            authors = book['volumeInfo']['authors']
            categories = book['volumeInfo'].get('categories')
            published_date = book['volumeInfo']['publishedDate'][0:4]
            average_rating = book['volumeInfo'].get('averageRating')
            ratings_count = book['volumeInfo'].get('ratingsCount')
            thumbnail = book['volumeInfo'].get('imageLinks')

            if thumbnail:
                thumbnail = thumbnail.get('thumbnail')
            existing = Book.objects.filter(title=title, authors__name=authors, published_date=published_date)
            if existing:
                identic = existing.objects.filter(categories=categories, average_rating=average_rating,
                                                  ratings_count=ratings_count, thumbnail=thumbnail)
                if not identic:
                    existing.update_categories()
                    existing.save(average_rating=average_rating,
                                  ratings_count=ratings_count, thumbnail=thumbnail)

            else:
                new_book = Book(title=title, published_date=published_date,
                                average_rating=average_rating,
                                ratings_count=ratings_count, thumbnail=thumbnail)
                new_book.save()
                new_book.update_categories(categories)
                new_book.add_authors(authors)

        serializer = BookSerializer()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Book.objects.filter(id=id)
