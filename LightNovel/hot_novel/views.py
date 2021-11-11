from hot_novel.models import HotNovel
from hot_novel.serializers import HotNovelSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny,IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.versioning import URLPathVersioning
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
class HotNovelListView(GenericAPIView):
    """
    列表视图
    """
    queryset = HotNovel.objects.all()  # 指定查询集
    serializer_class = HotNovelSerializer  # 指定序列化器类

    permission_classes = [IsAuthenticated]  # 允许所有用户访问
    filter_backends = [DjangoFilterBackend]  # 指定过滤器
    filterset_fields = ['id', 'author', 'classification']  # 指定需要过滤的字段
    versioning_class = URLPathVersioning  # 指定版本控制相关的类

    def get(self, request, *args, **kwargs):
        version = request.version
        if version == 'v1':
            hot_novels = self.get_queryset()  # 获取查询集的内容
            hot_novels = self.filter_queryset(hot_novels)  # 过滤字段
            page = self.paginate_queryset(hot_novels)  # 分页
            if page is not None:
                serializer = self.get_serializer(page, many=True)  # 传入分页后的数据给序列化器，获取一个1实列
                return self.get_paginated_response(serializer.data)  # 返回分页后的数据
            serializer = self.get_serializer(hot_novels, many=True)  # 直接传入数据，获取序列化器的实列
            return Response(serializer.data)  # 返回内容

    def post(self, request):
        data = request.data  # 获取到前端的数据
        if isinstance(data, dict):  # 判断前端传来的数据格式为字典，即只有一个数据
            many = False
        elif isinstance(data, list):  # 前端传来的数据为列表，即有很多数据
            many = True
        else:
            raise exceptions.ValidationError('数据格式不正确!!!')
        serializer = self.get_serializer(data=data, many=many)  # 传入数据，获取序列化器的实列
        serializer.is_valid(raise_exception=True)  # 校验字段，可以自行在序列化器中写校验方法，如果有错，直接报错，不会再执行下面的save
        serializer.save()  # is_valid如果没报错，就直接保存数据
        return Response(serializer.data)  # 返回post的数据


class HotNovelDetailView(GenericAPIView):
    """
    详情视图
    """
    queryset = HotNovel.objects.all()  # 指定查询集
    serializer_class = HotNovelSerializer  # 指定序列化器类
    permission_classes = [AllowAny]  # 允许所有用户访问

    def get(self, request, pk):
        """
        查询单个id
        """
        data = self.get_object()  # 获取查询到的单个id数据
        serializer = self.get_serializer(data)  # 传入查询到的数据，获取序列化器实列
        return Response(serializer.data)  # 返回查询到的单个id的值

    def put(self, request, pk):
        """
        修改单个id
        """
        data = self.get_object()  # 获取查询的单个id数据
        serializer = self.get_serializer(data, request.data)  # 传入数据，获取序列化器实列
        serializer.is_valid(raise_exception=True)  # 校验字段
        serializer.save()  # 保存数据
        return Response(serializer.data)  # 返回修改的数据

    def delete(self, request, pk):
        """
        删除单个id
        """
        data = self.get_object()  # 获取查询的单个id数据
        data.delete()  # 删除查询到的数据
        return Response(status=status.HTTP_204_NO_CONTENT)  # 返回删除后的状态码


class Blog(GenericAPIView):
    """
    博客路由
    """
    queryset = HotNovel.objects.all()  # 指定查询集
    serializer_class = HotNovelSerializer  # 指定序列化器类

    permission_classes = [AllowAny]  # 允许所有用户访问
    filter_backends = [DjangoFilterBackend]  # 指定过滤器
    filterset_fields = ['id', 'author', 'classification']  # 指定需要过滤的字段
    versioning_class = URLPathVersioning  # 指定版本控制相关的类


def index(request):
    """
    函数视图，返回模板文件中的html
    """
    return render(request, 'hot_novel/index.html')
