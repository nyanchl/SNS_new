from django.urls import path
from . import views
from . import config
from app.views import SampleAPIView,TemplateView


app_name = 'sns'

urlpatterns = [
    path("sample/", SampleAPIView.as_view(), name="sample"),
    
    path('',views.BaseView.as_view(),name='base'),
    path('',views.BaseUserView.as_view(),name='base'),
    path('post/', views.TextCreateView.as_view(), name='post'),
    path('delete/<int:pk>', views.TextDeleteView, name='delete_text'),
    path('edit/<int:pk>', views.TextEditView.as_view(), name='edit_text'),

    path('config/', TemplateView.as_view(template_name="../templates/config.html"), name='config'),
    path('config/negaposi',config.get_negaposi_flag, name='negaposi'),

    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('comment_detail/<int:pk>', views.CommentDetailView.as_view(), name='comment_detail'),

    path('like_for_post/', views.like_for_post, name='like_for_post'),
    path('like_for_comment/', views.like_for_comment, name='like_for_comment'),

    path('comment/create/<int:pk>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('commenttocomment/create/<int:pk>/', views.CommentToCommentCreateView.as_view(), name='commenttocomment_create'),

    path('profile/<str:name>/', views.ProfileView, name='profile'),
    path('profile/<str:name>/edit', views.ProfileEditView, name='edit_bio'),
    path('profile/<str:name>/follow', views.FollowView, name='follow'),
    path('profile/<str:name>/unfollow', views.UnFollowView, name='unfollow'),

    path('notice/', views.Notice_index.as_view(), name='notice'),
    ]