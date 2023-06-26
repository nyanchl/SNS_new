"""sns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import activate_user
from app.views import ProfileView,ProfileEditView,CommentDetailView,FrontBaseView,LoginBaseView

from rest_framework_simplejwt import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('home/', FrontBaseView.as_view()),
    path('vuelogin',LoginBaseView.as_view()),

    path('accounts/',include('accounts.urls')),
    path('users/<uuid:activate_token>/activation/', activate_user, name='users-activation'),
    path('', include('app.urls')),
    path('profile/<str:name>/', ProfileView, name='profile'),
    path('comment_detail/<int:pk>', CommentDetailView.as_view(), name='comment_detail'),
    path('<str:name>/edit', ProfileEditView, name='edit_bio'),

    #アプリのapiのルーティング
    path('api/', include('api.urls')),

    #jwt-tokenの取得
    path('api-auth/jwt', views.TokenObtainPairView.as_view()),
    #jwt-tokenの再取得
    path('api-auth/jwt/refresh', views.TokenRefreshView.as_view()),
]