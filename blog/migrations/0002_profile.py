# Generated by Django 3.2 on 2021-06-04 21:10

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('surname', models.CharField(max_length=25)),
                ('about_me', models.TextField(blank=True)),
                ('avatar', models.ImageField(blank=True, upload_to=blog.models.user_directory_path)),
                ('user', models.OneToOneField(max_length=25, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
