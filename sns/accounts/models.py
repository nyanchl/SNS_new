from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid as uuid_lib
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime, timedelta

import uuid

class AuthUserManager(BaseUserManager):
    def create_user(self, username, email, password, name ):
        """
        ユーザ作成
        username
        email
        password
        """
        if not email:
            raise ValueError(_('Users must have an email'))
        
        user = self.model(email=email,
                          password=password,
                          username=username,
                          name=name,)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self,username,email,password,name):
        #スーパユーザ作成

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                name=name,)
        user.admin = True
        user.save(using=self._db)
        return user


class AuthUser(AbstractBaseUser):
    """
    user設定
    認証方法 email,password
    unique=true name
    username
    """

    class Meta:
        db_table = 'user'
        verbose_name = 'User'

    username = models.CharField(verbose_name='username', null=False,unique=True,max_length=30)
    name = models.CharField(verbose_name='name',primary_key=True,unique=True,max_length=15)
    email = models.EmailField(verbose_name='email',unique=True)
    password = models.CharField(max_length=1024, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(verbose_name='管理サイトアクセス権限', default=False)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','name']

    objects = AuthUserManager()


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.admin

    @property
    def date_joined(self):
        return self.date_joined

    def __str__(self):
        return self.name

class RelateUser(models.Model):
    class Meta:
        db_table = 'relateuser'
        verbose_name = 'relateuser'
    

    follow_target = models.ForeignKey(AuthUser, related_name='follow_target', on_delete=models.CASCADE)
    owner = models.ForeignKey(AuthUser, related_name="owner", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.owner.username, self.follow_target.username)

class Profile(models.Model):
    class Meta:
        db_table = 'profile'
        verbose_name = 'Profile'

    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, primary_key=True)
    text = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.user.name

    @property
    def followers(self):
        return RelateUser.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return RelateUser.objects.filter(user=self.user).count()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()

        
@receiver(post_save, sender=AuthUser)
def create_profile(sender, **kwargs):
    """ 新規ユーザー作成時に空のprofileも作成する """
    if kwargs['created']:
        user_profile = Profile.objects.get_or_create(user=kwargs['instance'])


#-------------------------メール認証-------------------------------
class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, activate_token):
        user_activate_token = self.filter(
            activate_token=activate_token,
            expired_at__gte=datetime.now()
        ).first()
        if hasattr(user_activate_token, 'user'):
            user = user_activate_token.user
            user.is_active = True
            user.save()
            return user
        
class UserActivateTokens(models.Model):

    token_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activate_token = models.UUIDField(default=uuid.uuid4)
    expired_at = models.DateTimeField()

    objects = UserActivateTokensManager()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def publish_activate_token(sender, instance, **kwargs):
    if not instance.is_active:
        user_activate_token = UserActivateTokens.objects.create(
            user=instance,
            expired_at=datetime.now()+timedelta(days=settings.ACTIVATION_EXPIRED_DAYS),
        )
        subject = 'Please Activate Your Account'
        message = f'URLにアクセスしてユーザーアクティベーション。\n http://127.0.0.1:8000/users/{user_activate_token.activate_token}/activation/'
    if instance.is_active:
        subject = 'Activated! Your Account!'
        message = 'ユーザーが使用できるようになりました'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [
        instance.email,
    ]
    send_mail(subject, message, from_email, recipient_list)