from django.conf.urls import url
from hot_novel import views
from django.urls import path

urlpatterns = [

    #  注意:匹配创建的路由时，最好加上开始符^和结束符$，不然可能会一直在匹配这个路由

    url('^hot_novel/$', views.HotNovelListView.as_view()),  # 匹配创建的列表视图路由
    url(r'^(?P<version>[v1|v2]+)$/hot_novel', views.HotNovelListView.as_view()),  # 匹配版本控制相关的路由
    url(r'^hot_novel/(?P<pk>\d+)/$', views.HotNovelDetailView.as_view()),  # 匹配创建的详情视图的路由
    url(r'^blog/$',views.index)  # 匹配创建的blog函数视图
]
