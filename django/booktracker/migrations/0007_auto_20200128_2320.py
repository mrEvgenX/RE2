# Generated by Django 3.0.2 on 2020-01-28 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booktracker', '0006_set_existing_books_shelves'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelvedbook',
            name='shelf',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='booktracker.Shelf'),
        ),
    ]
