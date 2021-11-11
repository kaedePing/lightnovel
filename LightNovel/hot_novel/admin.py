from django.contrib import admin
from hot_novel import models

# Register your models here.
admin.site.register(models.HotNovel)  # 在app中注册模型，这样在后台可视化管理中，就可以直接看到该模型对应的数据
