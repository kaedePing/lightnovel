from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from account.serializers import AccountSerializer
from rest_framework import status
from rest_framework import exceptions
from django.contrib.auth import hashers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token


# Create your views here.
class Register(GenericAPIView):
    """
    注册用户的视图
    """
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get(self, request):
        data = self.get_queryset()
        return Response(status.HTTP_403_FORBIDDEN)  # 返回403禁止访问这个路由

    def post(self, request):
        data = request.data
        if isinstance(data, dict):  # 一次只能创建一个用户，其他情况直接400
            many = False
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)  # 校验是否合法
        serializer.save()
        user = {
            'username': serializer.data['username'],  # 返回用户名
            'is_active': serializer.data['is_active']  # 返回密码
        }
        return Response(user)


class DeleteUser(GenericAPIView):
    """
    删除用户的视图
    """
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    @staticmethod
    def is_existence(self, request):
        existence = True  # 原始设置为True,不存在用户,密码不对都设置为False
        data = request.data
        username = data['username']
        password = data['password']
        result_factual = User.objects.filter(username=username)  # 筛选是否存在该用户
        if len(result_factual) == 1:
            result = self.get_queryset()  # 找到表中所有用户
            result = self.get_serializer(result, many=True)
            for i in result.data:  # 循环找到前端传来的user信息
                if username == i['username']:
                    temp_password = i['password']
                    if hashers.check_password(password, temp_password):  # 密码存在，校验通过,执行删除
                        result_factual.delete()  # 将查询到的用户结果删除
                    else:
                        raise exceptions.ValidationError('密码不正确!')
                        existence = False
                    break
                else:
                    pass

        else:
            raise exceptions.ValidationError('不存在该用户!')
            existence = False  # 不存在该用户，设置为False

        return existence

    def delete(self, request):
        if self.is_existence(self, request=request):
            detail = request.data['username'] + '已被删除！'
            return Response(detail)


class DeleteToken(GenericAPIView):
    queryset = Token.objects.all()

    permission_classes = [AllowAny]

    @staticmethod
    def delete_one_or_delete_all(self, request):
        """
        删除token
        """
        token = request.auth
        user = request.user
        if token is not None:
            """
            如果前端传来一个参数token，则删除单个，否则删除所有token
            """
            data = Token.objects.filter(key=token)
            if len(data) == 1:
                data.delete()
                return str(token) + '已被删除！'
            else:
                raise exceptions.ValidationError('不存在的token!')
        else:
            Token.objects.all().delete()
            return '所有token已被删除！'

    def delete(self, request):
        text = self.delete_one_or_delete_all(self, request)
        if text:
            return Response(text)