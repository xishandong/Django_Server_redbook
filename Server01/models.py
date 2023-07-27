from django.db import models
from webServer.settings import SYSTEM_PATH
from Server01.util.auxiliaryFuction import check_and_delete


class User(models.Model):
    """ 用户表 """
    email = models.CharField(max_length=32, verbose_name='邮箱', null=False, default='123@123.com')
    username = models.CharField(max_length=32, verbose_name='用户名', null=False)
    password = models.CharField(max_length=64, verbose_name='密码', null=False)
    avatar = models.CharField(max_length=256, verbose_name='头像', null=False,
                              default='http://localhost:8000/static/img/avatar/defaultAvatar.jpg')
    signature = models.CharField(max_length=64, verbose_name='个性签名', default='暂时没有个性签名~', null=True)
    # 用户关注，related_name获取用户的粉丝
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='beFocusOn')
    # 用户喜爱的帖子
    favorites = models.ManyToManyField('Post', blank=True, related_name='favoritePosts')
    # 用户收藏的帖子
    collected = models.ManyToManyField('Post', blank=True, related_name='collectedPosts')


class Post(models.Model):
    """ 帖子表 """
    # 用户通过related_name获取ta发的帖子
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=64, verbose_name='标题', null=False)
    content = models.TextField(max_length=3000, verbose_name='内容', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def delete(self, *args, **kwargs):
        # 删除关联的帖子图片
        self.imgs.all().delete()
        # 删除帖子的图片的存储
        path = SYSTEM_PATH + 'post/'
        check_and_delete(mainPath=path, id=self.id)
        # 删除帖子本身
        super().delete(*args, **kwargs)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='imgs')
    imagePath = models.CharField(max_length=256, verbose_name='帖子图片')
    height = models.IntegerField(default=0, verbose_name='图片高度')
    width = models.IntegerField(default=0, verbose_name='图片宽度')


class Comment(models.Model):
    """ 评论表 """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=3000, verbose_name='评论', null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
