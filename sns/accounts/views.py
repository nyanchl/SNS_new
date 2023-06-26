from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import UserActivateTokens

from .models import AuthUser

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

def activate_user(request, activate_token):
    print("hoge")
    activated_user = UserActivateTokens.objects.activate_user_by_token(
        activate_token)
    if hasattr(activated_user, 'is_active'):
        if activated_user.is_active:
            message = 'ユーザーのアクティベーションが完了しました'
        if not activated_user.is_active:
            message = 'アクティベーションが失敗しています。管理者に問い合わせてください'
    if not hasattr(activated_user, 'is_active'):
        message = 'エラーが発生しました'
    return HttpResponse(message)

#フロント側ログイン
class LoginBaseView(TemplateView):
    """フロント側のログイン画面"""

    template_name = "index.html"