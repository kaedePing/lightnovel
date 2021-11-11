from django.db import models


# Create your models here.
class HotNovel(models.Model):
    title = models.CharField(max_length=100, default=None)  # 标题
    classification = models.CharField(max_length=100, default=None)  # 文库分类
    author = models.CharField(max_length=100, default=None)  # 作者
    status = models.CharField(max_length=100, default=None)  # 小说状态
    update = models.DateField(default=None)  # 最后更新
    length = models.IntegerField(default=0)  # 文章长度
    cover = models.URLField(default='http://www.wenku8.net/index.php')  # 小说封面

    class Meta:
        db_table = 'hot_novel'  # 存储的数据表名
