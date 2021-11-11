from rest_framework.serializers import ModelSerializer
from hot_novel.models import HotNovel
from rest_framework import exceptions


class HotNovelSerializer(ModelSerializer):
    class Meta:
        model = HotNovel  # 指定需要校验的模型
        fields = '__all__'  # 校验所有字段

    def validate(self, attrs):
        """
        自定义校验方法，需返回同样的参数
        """
        return attrs


