from books_api.serializers import BookSerializer
from books_api.models import Book
import requests
from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework import generics

class BookFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="authors__name", lookup_expr='contains')
    sort = filters.OrderingFilter(
        fields=(
            ('published_date', 'published_date')
        )
    )

    class Meta:
        model = Book
        fields = ['published_date']

class BookViewSet(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter

    def post(self, request):
        q = request.query_params.get('q')
        if q:
            url = f'https://www.googleapis.com/books/v1/volumes?q={q}'
            r = requests.get(url)
            books = r.json()['items']
            for book in books:
                title = book['volumeInfo']['title']
                authors = book['volumeInfo'].get('authors', [])
                categories = book['volumeInfo'].get('categories')
                published_date = int(book['volumeInfo']['publishedDate'][:4]) if book['volumeInfo'].get('publishedDate',False) else False
                average_rating = book['volumeInfo'].get('averageRating', None)
                ratings_count = book['volumeInfo'].get('ratingsCount', None)
                thumbnail = book['volumeInfo']['imageLinks'].get('thumbnail', None) if book['volumeInfo'].get('imageLinks', False) else False
                get_book = Book.objects.safe_get(
                        title=title,
                        published_date=published_date)
                if get_book and get_book.compare_authors(authors):
                    get_book.average_rating = average_rating
                    get_book.ratings_count = ratings_count
                    get_book.thumbnail = thumbnail
                    get_book.save()
                else:
                    new_book = Book(title=title,
                        published_date=published_date,
                        average_rating=average_rating,
                        ratings_count=ratings_count,
                        thumbnail=thumbnail)
                    new_book.save()
                    new_book.add_authors(authors)
                    new_book.update_categories(categories)
        library = Book.objects.all().distinct()
        serializer = BookSerializer(library, many=True)
        return Response(serializer.data)


class BookView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return [Book.objects.get(id=id)]
