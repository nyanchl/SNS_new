from django.db import models
from accounts.models import AuthUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class MyText(models.Model):
    """投稿モデル"""
    class Meta:
        db_table = 'mytext'

    user = models.ForeignKey(AuthUser,on_delete=models.CASCADE)
    text = models.TextField(max_length=255,null=False,blank=False)
    # image = models.ImageField(upload_to='img/',blank=True, null=True)
    textpoint = models.FloatField(verbose_name='textpoint',validators=[MinValueValidator(-100.000000), MaxValueValidator(100.000000)],blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    

class Comment(models.Model):
    """コメントモデル"""
    class Meta:
        db_table = 'comment'
    
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    comment_text = models.TextField('コメント')
    commentpoint = models.FloatField(validators=[MinValueValidator(-100.000000), MaxValueValidator(100.000000)],blank=True, null=True)
    target_text = models.ForeignKey(MyText,verbose_name='対象投稿',on_delete=models.CASCADE,blank=True, null=True)
    target_comment = models.ForeignKey('self',verbose_name='対象コメント',on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return self.comment_text

class LikeForPost(models.Model):
    """いいねモデル(投稿)"""
    class Meta:
        db_table = 'like'

    target = models.ForeignKey(MyText, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.target

    
class LikeForComment(models.Model):
    """いいねモデル(コメント)"""
    class Meta:
        db_table = 'commetforlike'

    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.target
    

class Notice(models.Model):
    """通知"""
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    # notice_count = models.IntegerField(default=0)
    text = models.TextField()
    comment = models.TextField()

@receiver(post_save, sender=AuthUser)
def create_profile(sender, **kwargs):
    """ 新規ユーザー作成時に空の通知モデルを作成する """
    if kwargs['created']:
        user_notice = Notice.objects.get_or_create(user=kwargs['instance'])