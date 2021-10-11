from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=400)

    def __str__(self):
        return self.title

class BookManager(models.Manager):
    def safe_get(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except Book.DoesNotExist:
            return False

class Book(models.Model):
    objects = BookManager()
    title = models.CharField(max_length=400)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    published_date = models.IntegerField(default=0)
    average_rating = models.IntegerField(default=0, null=True)
    ratings_count = models.IntegerField(default=0, null=True)
    thumbnail = models.URLField(max_length=2000, null=True)

    def add_authors(self, new_authors):
        for author in new_authors:
            try:
                a_obj = Author.objects.get(name=author)
            except:
                a_obj = Author.objects.create(name=author)
            self.authors.add(a_obj)

    def compare_authors(self, authors):
        current = self.authors.values_list('name', flat=True)
        for author in authors:
            if author not in current:
                return False
        return True

    def update_categories(self, new_categories):
        if new_categories:
            self.categories.clear()
            for category in new_categories:
                try:
                    c_obj = Category.objects.get(title=category)
                except:
                    c_obj = Category.objects.create(title=category)
                self.categories.add(c_obj)
