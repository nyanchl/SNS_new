from typing import Any, Dict
from django.db.models import Count
from django.forms.models import model_to_dict
from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from django.views.generic import CreateView,ListView,DetailView,TemplateView,UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import TextForm,ProfileEditForm,CommentCreateForm,TextEditForm,CommentToCommentCreateForm
from .models import MyText,Comment,LikeForPost,LikeForComment,Notice,User_config
from accounts.models import AuthUser,Profile,RelateUser

from app.Analysis import analysisoutput
from app.AnalysisComment import analysiscomment

import pprint
import json
import numpy as np


class BaseView(LoginRequiredMixin,ListView):
    """ホーム画面"""
    model = MyText
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        user = User_config.objects.get(user=self.request.user)
        notice_user = Notice.objects.filter(user=self.request.user)

        #通知機能
        negatext = MyText.objects.filter(user=self.request.user, textpoint__lte=-0.49).count()
        negacomment = Comment.objects.filter(user=self.request.user, commentpoint__lte=-0.49).count()
        notice_user.update(text=negatext,comment=negacomment)

        negaposi_flag = user.config
        if negaposi_flag == False:
            context = super().get_context_data(**kwargs)
            context['like_for_post'] = LikeForPost.objects.all()
            postdata = MyText.objects.all().annotate(like=Count("likeforpost",direct=True)).order_by('created_datetime').reverse()
            context['postdata'] = postdata
            context['notice_count'] = negatext + negacomment
            if LikeForPost.objects.filter(user=self.request.user).exists():
                context['is_user_liked_for_post'] = True
            else:
                context['is_user_liked_for_post'] = False
        
        else:
            context = super().get_context_data(**kwargs)
            context['like_for_post'] = LikeForPost.objects.all()
            postdata = MyText.objects.filter(textpoint__gte=-0.49).annotate(like=Count("likeforpost",direct=True)).order_by('created_datetime').reverse()
            context['postdata'] = postdata
            context['notice_count'] = negatext + negacomment
            if LikeForPost.objects.filter(user=self.request.user).exists():
                context['is_user_liked_for_post'] = True
            else:
                context['is_user_liked_for_post'] = False

        return context
    

class BaseUserView(ListView):
    model = AuthUser
    template_name = 'base.html'


class PostDetailView(generic.DetailView):
    """投稿詳細"""
    template_name = 'detail.html'
    model = MyText

    def get_context_data(self,**kwargs):
        user = User_config.objects.get(user=self.request.user)
        negaposi_flag = user.config
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm
        postdata = self.object.likeforpost_set.count()
        context['postdata'] = postdata
        context['comments'] = self.object.comment_set.all()
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.likeforpost_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        d = {}
        if negaposi_flag == False:
            context['comments'] = self.object.comment_set.all()
            for comment in self.object.comment_set.all():
                like_for_comment_count = comment.likeforcomment_set.count()
                if comment.likeforcomment_set.filter(user=self.request.user).exists():
                    is_user_liked_for_comment = True
                else:
                    is_user_liked_for_comment = False
                d[comment.pk] = {'count':like_for_comment_count,'is_user_liked_for_comment':is_user_liked_for_comment}

                context[f'comment_like_data'] = d
        else:
            context['comments'] = self.object.comment_set.filter(commentpoint__gte=-0.49)
            for comment in self.object.comment_set.all():
                like_for_comment_count = comment.likeforcomment_set.count()
                if comment.likeforcomment_set.filter(user=self.request.user).exists():
                    is_user_liked_for_comment = True
                else:
                    is_user_liked_for_comment = False
                d[comment.pk] = {'count':like_for_comment_count,'is_user_liked_for_comment':is_user_liked_for_comment}

                context[f'comment_like_data'] = d
        
        return context


class CommentDetailView(generic.DetailView):
    """コメント詳細"""
    template_name = 'commentdetail.html'
    model = Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commenttocomment_form'] = CommentToCommentCreateForm
        commentdata = self.object.likeforcomment_set.count()
        context['commentdata'] = commentdata
        return context


class CommentCreateView(generic.CreateView):
    """コメント作成"""
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):

        text_pk = self.kwargs.get('pk')
        text = get_object_or_404(MyText, pk=text_pk)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.target_text = text
        #----------------------------------------MeCab---------------------------------------
        commenttex = model_to_dict(comment)                                     
        jsontext = json.dumps(commenttex)
        jsonloadtext = json.loads(jsontext)
        comment.commentpoint = analysiscomment(jsonloadtext['comment_text'])

        comment.save()
        
        return redirect('sns:post_detail', pk=text_pk)
    

class CommentToCommentCreateView(generic.CreateView):
    """コメント作成(コメント)"""
    model = Comment
    form_class = CommentToCommentCreateForm

    def form_valid(self, form):
        comment_pk = self.kwargs.get('pk')
        comment = get_object_or_404(Comment, pk=comment_pk)
        commenttocomment = form.save(commit=False)
        commenttocomment.user = self.request.user
        commenttocomment.target_comment = comment
        commenttocomment.save()

        return redirect('sns:comment_detail', pk=comment_pk)


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
    """投稿削除"""
    texts = get_object_or_404(MyText, pk=pk)
    texts.delete()
    return redirect('sns:base')


class TextEditView(generic.UpdateView):
    """投稿編集"""
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


def like_for_post(request):
    """いいね(投稿)"""
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
    """いいね(コメント)"""
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


def ProfileView(request,name):
    """プロフィール"""
    user = get_object_or_404(AuthUser,pk=name)
    profile = Profile.objects.get(user=user)
    text = MyText.objects.filter(user=user)
    comment = Comment.objects.filter(user=user)
    likeforpost = LikeForPost.objects.all()
    postdata = MyText.objects.filter(user=user).annotate(like=Count("likeforpost",direct=True))
    mylike = LikeForPost.objects.filter(user_id=user)
    commentmylike = LikeForComment.objects.filter(user_id=user)
    
    context = {
        'user':user,
		'profile':profile,
        'name':name,
        'text':text,
        'comment':comment,
        'postdata':postdata,
        'likeforpost':likeforpost,
        'mylike':mylike,
        'commentmylike':commentmylike,
	}

    result = RelateUser.objects.filter(owner=request.user.name).filter(follow_target=context['user'].name).count()
    context['connected'] = True if result else False
    context['test'] = result
    context['test2'] = context['user'].name
    context['test3'] = request.user.name

    return render(request, 'profile.html', context)


def ProfileEditView(request,name):
    """プロフィール編集"""
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

    
@login_required
def FollowView(request,*args,**kwargs):
    """フォロー"""
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
    """フォロー解除"""
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


class Notice_index(TemplateView):
    template_name = 'notice.html'
    model = MyText

    def get(self, request, **kwargs):
        get_mytext_negative = MyText.objects.filter(textpoint__lte= -0.49)
        get_comment_negative = Comment.objects.filter(commentpoint__lte= -0.49)
        user_name = request.user

        context = {'user_name': user_name,
                   'texts': get_mytext_negative,
                   'comments': get_comment_negative
                   }

        return render(request, 'notice.html', context)
    

class SampleAPIView(APIView):

    def get(self, request):
        return Response("OK", status=status.HTTP_200_OK)
    

class FrontBaseView(TemplateView):

    template_name = "index.html"
