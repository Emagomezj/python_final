# Generated by Django 4.2 on 2024-09-04 02:32

import blogs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_blog_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog_img',
            name='image',
            field=models.ImageField(blank=True, default='blogs_imgs/default_blog_img.jpg', null=True, upload_to=blogs.models.get_random_filename),
        ),
    ]
