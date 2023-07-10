from django.db import models


class User(models.Model):
    """ 用户表 """
    email = models.CharField(max_length=32, verbose_name='邮箱', null=False, default='123@123.com')
    username = models.CharField(max_length=32, verbose_name='用户名', null=False)
    password = models.CharField(max_length=64, verbose_name='密码', null=False)
    avatar = models.CharField(max_length=256, verbose_name='头像', null=False,
                              default='http://localhost:8000/static/img/avatar/defaultAvatar.jpg')
    signature = models.CharField(max_length=64, verbose_name='个性签名', default='暂时没有个性签名~', null=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='beFocusOn')
    followed = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='focusOn')
    favorites = models.ManyToManyField('Post', blank=True, related_name='favoritePosts')
    collected = models.ManyToManyField('Post', blank=True, related_name='collectedPosts')


class Post(models.Model):
    """ 帖子表 """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=64, verbose_name='标题', null=False)
    content = models.TextField(max_length=3000, verbose_name='内容', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def delete(self, *args, **kwargs):
        # 删除关联的帖子图片
        self.imgs.all().delete()

        # 删除帖子本身
        super().delete(*args, **kwargs)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='imgs')
    imagePath = models.CharField(max_length=256, verbose_name='帖子图片')


class Comment(models.Model):
    """ 评论表 """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=3000, verbose_name='评论', null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
