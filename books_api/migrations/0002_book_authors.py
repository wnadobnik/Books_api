# Generated by Django 3.2.4 on 2021-06-18 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(to='books_api.Author'),
        ),
    ]
