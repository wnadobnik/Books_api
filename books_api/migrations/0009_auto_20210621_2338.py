# Generated by Django 3.2.4 on 2021-06-21 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0008_alter_book_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='average_rating',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='ratings_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
