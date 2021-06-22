from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=400)

    def __str__(self):
        return self.title

class Book(models.Model):
    title = models.CharField(max_length=400)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    published_date = models.IntegerField(default=0)
    average_rating = models.IntegerField(default=0, null=True)
    ratings_count = models.IntegerField(default=0, null=True)
    thumbnail = models.URLField(max_length=2000, null=True)

    def add_authors(self, new_authors):
        for author in new_authors:
            if not self.authors.filter(name=author):
                if not Author.objects.filter(name=author):
                    self.authors.create(name=author)
                else:
                    self.authors.add(Author.objects.get(name=author))

    def update_categories(self, new_categories):
        if new_categories:
            self.categories.clear()
            for category in new_categories:
                if not Category.objects.filter(title=category):
                    self.categories.create(title=category)
                else:
                    self.categories.add(Category.objects.get(title=category))
