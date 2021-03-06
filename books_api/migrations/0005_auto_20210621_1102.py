# Generated by Django 3.2.4 on 2021-06-21 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0004_auto_20210621_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(related_name='authors', to='books_api.Book'),
        ),
        migrations.AddField(
            model_name='category',
            name='books',
            field=models.ManyToManyField(related_name='titles', to='books_api.Book'),
        ),
    ]
