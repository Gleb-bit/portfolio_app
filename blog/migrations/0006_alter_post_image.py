# Generated by Django 3.2.4 on 2021-07-10 12:54

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=blog.models.post_directory_path),
            preserve_default=False,
        ),
    ]