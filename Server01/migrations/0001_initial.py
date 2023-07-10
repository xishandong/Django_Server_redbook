# Generated by Django 4.1 on 2023-07-09 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=64, verbose_name="标题")),
                (
                    "content",
                    models.TextField(max_length=3000, null=True, verbose_name="内容"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=32, verbose_name="用户名")),
                ("password", models.CharField(max_length=64, verbose_name="密码")),
                (
                    "avatar",
                    models.CharField(
                        default="http://localhost:8000/static/img/defaultAvatar.jpg",
                        max_length=64,
                        null=True,
                        verbose_name="头像",
                    ),
                ),
                (
                    "signature",
                    models.CharField(
                        default="暂时没有个性签名~",
                        max_length=64,
                        null=True,
                        verbose_name="个性签名",
                    ),
                ),
                (
                    "collected",
                    models.ManyToManyField(
                        blank=True, related_name="collected", to="Server01.post"
                    ),
                ),
                (
                    "favorites",
                    models.ManyToManyField(
                        blank=True, related_name="favorite", to="Server01.post"
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True, related_name="followers", to="Server01.user"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="Server01.user",
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(max_length=3000, verbose_name="评论")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                (
                    "parent_comment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="Server01.comment",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="Server01.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="Server01.user",
                    ),
                ),
            ],
        ),
    ]