from django.urls import path,include
from . import views

urlpatterns = [
    path('text/', include(views.router.urls)),  
]