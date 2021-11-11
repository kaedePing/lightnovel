from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from account import views

urlpatterns = [
    url('account/token', obtain_auth_token),  # 调用drf的下自带的token验证登录,传入username、password可以直接生成token
    url('account/register', views.Register.as_view()),  # 调用创建的Register路由，包括get和post
    url('account/delete$', views.DeleteUser.as_view()),  # 调用创建的DeleteUser路由，只有delete方法
    url('account/token/delete', views.DeleteToken.as_view())  # 调用创建的DeleteToken路由
]
