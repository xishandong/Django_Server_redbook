# Generated by Django 4.1 on 2023-07-09 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Server01", "0006_image_post_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="imagePath",
            field=models.CharField(max_length=256, verbose_name="帖子图片"),
        ),
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.CharField(
                default="http://localhost:8000/static/img/avatar/defaultAvatar.jpg",
                max_length=256,
                verbose_name="头像",
            ),
        ),
    ]
