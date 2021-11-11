from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth import hashers


class AccountSerializer(ModelSerializer):
    class Meta:
        model = User  # 使用django自带的contrib.auth.models下的User
        fields = '__all__'

    def validate(self, attrs):
        attrs['password'] = hashers.make_password(attrs['password'])  # 将前端传来的password由auth加密

        return attrs
