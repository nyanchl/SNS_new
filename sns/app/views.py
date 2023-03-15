from .models import MyText,Comment,LikeForPost,LikeForComment
from accounts.models import AuthUser,Profile,RelateUser
from django.db.models import Count

from .forms import TextForm,ProfileEditForm,CommentCreateForm,TextEditForm
from django.forms.models import model_to_dict
from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.views.generic import CreateView,ListView,DetailView,TemplateView,UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from app.Analysis import analysisoutput
from app.AnlysisComment import analysiscomment

import pprint
import json
import numpy as np


#=================================default======================================================

class BaseView(LoginRequiredMixin,ListView):
    model = MyText
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        self.request
        context = super().get_context_data(**kwargs)
        context['like_for_post'] = LikeForPost.objects.all
        postdata = MyText.objects.all().annotate(like=Count("likeforpost",direct=True))
        context['postdata'] = postdata
        if LikeForPost.objects.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        return context
        

class BaseUserView(ListView):
    model = AuthUser
    template_name = 'base.html'

class PostDetailView(generic.DetailView):
    template_name = 'detail.html'
    model = MyText

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm
        postdata = self.object.likeforpost_set.count()
        context['postdata'] = postdata
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.likeforpost_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        d = {}
        for comment in self.object.comment_set.all():
            like_for_comment_count = comment.likeforcomment_set.count()
            if comment.likeforcomment_set.filter(user=self.request.user).exists():
                is_user_liked_for_comment = True
            else:
                is_user_liked_for_comment = False
            d[comment.pk] = {'count':like_for_comment_count,'is_user_liked_for_comment':is_user_liked_for_comment}

            context[f'comment_like_data'] = d
        
        return context


#=================================positive======================================================
querypoint = MyText.objects.filter(textpoint__gt='0.0')
print(querypoint)


#================TEXT&COMMENT CRUD================

class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):

        text_pk = self.kwargs.get('pk')
        text = get_object_or_404(MyText, pk=text_pk)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.target_text = text

        #--------mecab---------------------------------------------------------
        commenttex = model_to_dict(comment)                                     
        jsontext = json.dumps(commenttex)
        jsonloadtext = json.loads(jsontext)
        comment.commentpoint = analysiscomment(jsonloadtext['comment_text'])

        comment.save()
        
        return redirect('sns:post_detail', pk=text_pk)



@method_decorator(login_required, name='dispatch')
class TextCreateView(CreateView):
    """ 投稿作成 """
    template_name = 'post.html'
    form_class = TextForm
    model = MyText

    def get_form_kwargs(self):
        kwargs = super(TextCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        tex = model_to_dict(object)
        jsontext = json.dumps(tex)
        jsonloadtext = json.loads(jsontext)
        object.textpoint = analysisoutput(jsonloadtext["text"])

        object.save()
        return super().form_valid(form)
    
    success_url = reverse_lazy('sns:base')

def TextDeleteView(request,pk):
    texts = get_object_or_404(MyText, pk=pk)
    texts.delete()
    return redirect('sns:base')

class TextEditView(generic.UpdateView):
    model = MyText
    form_class = TextEditForm
    template_name = 'mytextedit.html'

    def form_valid(self, form):
        text_pk = self.kwargs.get('pk')
        text = get_object_or_404(MyText, pk=text_pk)
        edittext = form.save(commit=False)
        edittext.user = self.request.user
        edittext.target_text = text
        tex = model_to_dict(edittext)
        jsontext = json.dumps(tex)
        jsonloadtext = json.loads(jsontext)
        edittext.textpoint = analysisoutput(jsonloadtext["text"])
        
        edittext.save()
        
        return redirect('sns:edit_text', pk=text_pk)

#====================like====================

def like_for_post(request):
    text_pk = request.POST.get('text_pk')
    context = {
        'user': '{request.user.name}',
    }
    text = get_object_or_404(MyText, pk=text_pk)
    like = LikeForPost.objects.filter(target=text, user=request.user)
    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=text, user=request.user)
        context['method'] = 'create'

    context['postdata'] = LikeForPost.objects.filter(target=text).count()

    return JsonResponse(context)

def like_for_comment(request):
    comment_pk = request.POST.get('comment_pk')
    context = {
        'user': '{request.user.name}',
    }
    comment = get_object_or_404(Comment, pk=comment_pk)
    like = LikeForComment.objects.filter(target=comment, user=request.user)
    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=comment, user=request.user)
        context['method'] = 'create'

    context['like_for_comment_count'] = comment.likeforcomment_set.count()

    return JsonResponse(context)

#=====================profile=====================    

def ProfileView(request,name):
    """ profile """
    user = get_object_or_404(AuthUser,pk=name)
    profile = Profile.objects.get(user=user)
    text = MyText.objects.filter(user=user)
    context = {
        'user':user,
		'profile':profile,
        'name':name,
        'text':text,
	}
    result = RelateUser.objects.filter(owner=request.user.name).filter(follow_target=context['user'].name).count()
    context['connected'] = True if result else False
    context['test'] = result
    context['test2'] = context['user'].name
    context['test3'] = request.user.name

    return render(request, 'profile.html', context)

def ProfileEditView(request,name):
    user = get_object_or_404(AuthUser,pk=name)
    profile = Profile.objects.get(user=user)
    form = ProfileEditForm(request.POST,instance=profile)
    form.save()
    context = {
        'user':user,
		'profile':profile,
        'name':name,
        'form':form,
	}
    return render(request, 'edit.html', context)
    
#===========================follow==============================

@login_required
def FollowView(request,*args,**kwargs):

    try:
        owner = AuthUser.objects.get(name=request.user.name)
        follow_target = AuthUser.objects.get(name=kwargs['name'])
    except AuthUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['name']))
        return HttpResponseRedirect(reverse_lazy('sns:base'))
    if owner == follow_target:
        messages.warning(request, '自分自身はフォローできません')
    else:
        created = RelateUser.objects.get_or_create(owner=owner,follow_target=follow_target)

        if (created):
            messages.success(request, '{}をフォローしました'.format(follow_target.name))
        else:
            messages.success(request, 'あなたはすでに{}をフォローしています'.format(follow_target.name))
        return HttpResponseRedirect(reverse_lazy('sns:profile',kwargs={'name': follow_target.name}))

@login_required
def UnFollowView(request,*args, **kwargs):
    
    try:
        owner = AuthUser.objects.get(name=request.user.name)
        follow_target = AuthUser.objects.get(name=kwargs['name'])

        if owner == follow_target:
            messages.warning(request, '自分自身はフォローできません')

        else:
            unfollow = RelateUser.objects.get(owner=owner, follow_target=follow_target)
            unfollow.delete()
            messages.success(request, 'あなたは{}のフォローを外しました'.format(follow_target.name))
    except AuthUser.DoesNotExist:
        messages.warning(request, '{}は存在しません'.format(kwargs['name']))
        return HttpResponseRedirect(reverse_lazy('sns:base'))
    except RelateUser.DoesNotExist:
        messages.warning(request, 'あなたは{0}をフォローしませんでした'.format(follow_target.name))
    return HttpResponseRedirect(reverse_lazy('sns:profile', kwargs={'name': follow_target.name}))

class BaseFollowView(LoginRequiredMixin,ListView):
    model = RelateUser
    template_name = 'profile.html'