# Generated by Django 3.2.4 on 2021-06-21 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0006_auto_20210621_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='category',
            new_name='categories',
        ),
    ]
