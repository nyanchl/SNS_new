from django.urls import path,include
from .views import UserApiSet,LoginedUserSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register('text', UserApiSet)
router.register('user', LoginedUserSet)

urlpatterns = [
    path('', include(router.urls)),  
]