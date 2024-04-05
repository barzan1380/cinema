# Generated by Django 4.1.7 on 2024-01-01 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='is_given',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='seat',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie_seats', to='app.movie'),
        ),
    ]
