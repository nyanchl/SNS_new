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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import activate_user
from app.views import ProfileView,ProfileEditView,Comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('users/<uuid:activate_token>/activation/', activate_user, name='users-activation'),
    path('', include('app.urls')),
    path('<str:name>/', ProfileView, name='profile'),
    path('<int:id>/', Comment, name='comment_detail'),
    path('<str:name>/edit', ProfileEditView, name='edit_bio'),
]