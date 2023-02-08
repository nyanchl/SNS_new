from django import forms
from .models import MyText,Comment
from accounts.models import Profile
from django.db.models import Q

class TextForm(forms.ModelForm):
    class Meta:
        model = MyText
        exclude = ('user','name1','created_datetime','updated_datetime')
        widgets = {'text': forms.TextInput(attrs={'class': 'form-control'})}

    """https://codor.co.jp/django/about-qobject"""
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TextForm, self).__init__(*args, **kwargs)
        self.fields['text'].queryset = MyText.objects.filter(Q(user__isnull=True) |  Q(user=user))
        # self.fields['image'].queryset = MyText.objects.filter(Q(user__isnull=True) |  Q(user=user))

class SearchForm(forms.Form):
    key_word = forms.CharField(max_length=30, label='', required=False,widget=forms.TextInput(attrs={'placeholder': 'search username',}))

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('text',)

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)

class TextEditForm(forms.ModelForm):
    class Meta:
        model = MyText
        fields = ('text',)