from django.db import models
from accounts.models import AuthUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class MyText(models.Model):
    class Meta:
        db_table = 'mytext'

    user = models.ForeignKey(AuthUser,on_delete=models.CASCADE)
    text = models.TextField(max_length=255,null=False,blank=False)
    textpoint = models.FloatField(verbose_name='textpoint',validators=[MinValueValidator(-100.000000), MaxValueValidator(100.000000)],blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    

class Comment(models.Model):
    class Meta:
        db_table = 'comment'
    
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    comment_text = models.TextField('コメント')
    commentpoint = models.FloatField(validators=[MinValueValidator(-100.000000), MaxValueValidator(100.000000)],blank=True, null=True)
    target_text = models.ForeignKey(MyText,verbose_name='対象投稿',on_delete=models.CASCADE)


class LikeForPost(models.Model):
    class Meta:
        db_table = 'like'

    target = models.ForeignKey(MyText, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.target
    
    def __str__(self):
        return self.user
    

class LikeForComment(models.Model):
    class Meta:
        db_table = 'commetforlike'

    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.target
    
    def __str__(self):
        return self.user