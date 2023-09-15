from django.views.generic import TemplateView
from django.shortcuts import render

from app.models import User_config


def get_negaposi_flag(request):
    request_user = User_config.objects.get(user=request.user)
    if request.method == 'POST':
        if 'True' in request.POST:
            request_user.config = True
            request_user.save()
        elif 'False' in request.POST:
            request_user.config = False
            request_user.save()
    return render(request,"config.html")