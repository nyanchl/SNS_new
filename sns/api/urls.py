from django.urls import path,include
from .views import UserApiSet,UserViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register('text', UserApiSet)
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  
]