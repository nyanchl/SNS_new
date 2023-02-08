from curses.ascii import US
from django.contrib import admin
from .models import AuthUserManager,AuthUser,Profile,RelateUser

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = AuthUser
        fields = ('email','date_joined','admin','last_login')
        readonly_fields = ('date_joined')
    list_filter = ('admin',)
    ordering = ('email',)
    search_fields = ('email',)
admin.site.register(AuthUser,UserAdmin)
admin.site.register(RelateUser)
admin.site.register(Profile)