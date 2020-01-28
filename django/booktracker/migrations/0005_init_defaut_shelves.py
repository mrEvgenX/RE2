# Generated by Django 3.0.2 on 2020-01-28 15:28

from django.db import migrations


def create_default_shelves(apps, schema_editor):
    Shelf = apps.get_model('booktracker', 'Shelf')
    Shelf.objects.create(name='Want to read')
    Shelf.objects.create(name='Currently reading')
    Shelf.objects.create(name='Read')


class Migration(migrations.Migration):

    dependencies = [
        ('booktracker', '0004_auto_20200128_2224'),
    ]

    operations = [
        migrations.RunPython(create_default_shelves)
    ]
