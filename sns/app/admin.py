from curses.ascii import US
from django.contrib import admin
from .models import MyText,LikeForPost,Comment,LikeForComment,Notice,User_config
# Register your models here.
admin.site.register(MyText)
admin.site.register(LikeForPost)
admin.site.register(Comment)
admin.site.register(LikeForComment)
admin.site.register(Notice)
admin.site.register(User_config)