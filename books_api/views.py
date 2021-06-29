from books_api.serializers import BookSerializer
from books_api.models import Book
from rest_framework.views import APIView
import requests
from rest_framework.response import Response


class BookViewSet(APIView):
    serializer_class = BookSerializer


    def get(self, request, format=None):
        result = Book.objects.all()
        published_date = request.query_params.get('published_date')
        authors = request.query_params.getlist('author', '')
        sort = request.query_params.get('sort')
        if published_date:
            if isinstance(published_date, int) and len(published_date) <= 4:
                result = result.filter(published_date=published_date)
        if authors:
            result = result.filter(authors__name=authors)
        if sort == '-published_date' or sort == "published_date":
            result = result.order_by(sort)
        serializer = BookSerializer(result.distinct(), many=True)
        return Response(serializer.data)

    def post(self, request):
        books_standardized = []
        q = request.query_params.get('q')
        if q:
            url = f'https://www.googleapis.com/books/v1/volumes?q={q}'
            r = requests.get(url)
            books = r.json()['items']
            for book in books:
                books_standardized.append({
                    'title': book['volumeInfo']['title'],
                    'authors': book['volumeInfo']['authors'],
                    'categories': book['volumeInfo'].get('categories'),
                    'published_date': book['volumeInfo']['publishedDate'][0:4],
                    'average_rating': book['volumeInfo'].get('averageRating'),
                    'ratings_count': book['volumeInfo'].get('ratingsCount'),
                    'thumbnail': book['volumeInfo']['imageLinks'].get('thumbnail') if book['volumeInfo'].get(
                        'imageLinks') else None})
        else:
            books_standardized.append({
                'title': request.query_params.get('title'),
                'authors': request.query_params.get('authors').split(','),
                'categories': request.query_params.get('categories').split(','),
                'published_date': request.query_params.get('published_date'),
                'average_rating': request.query_params.get('average_rating'),
                'ratings_count': request.query_params.get('ratings_count'),
                'thumbnail': request.query_params.get('thumbnail')})

        for book_standardized in books_standardized:
            book_operate = Book.objects.filter(title=book_standardized['title'],
                                               authors__name=book_standardized['authors'],
                                               published_date=book_standardized['published_date'])
            if book_operate:
                book_operate.save(average_rating=book_standardized['average_rating'],
                                  ratings_count=book_standardized['ratings_count'],
                                  thumbnail=book_standardized['thumbnail'])
            else:
                book_operate = Book(title=book_standardized['title'],
                                    published_date=book_standardized['published_date'],
                                    average_rating=book_standardized['average_rating'],
                                    ratings_count=book_standardized['ratings_count'],
                                    thumbnail=book_standardized['thumbnail'])
                book_operate.save()
                book_operate.add_authors(book_standardized['authors'])
            book_operate.update_categories(book_standardized['categories'])
        library = Book.objects.all().distinct()
        serializer = BookSerializer(library, many=True)
        return Response(serializer.data)


class BookView(APIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        return Book.objects.get(id=id)
