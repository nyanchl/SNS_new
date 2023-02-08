from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import AuthUser
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
class RegisterForm(UserCreationForm):
    class Meta:
        model = AuthUser
        fields = ('email','username','name')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sns:base')
    else:
        form = RegisterForm()
    return render(request, 'signup.html',{'form':form})