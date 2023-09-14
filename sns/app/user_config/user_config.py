from app.models import User_config

class User_Config:
    def get_negaposi_flag(request, flag):
        request_user = User_config.objects.filter(user=request.user)
        if flag == True:
            request_user.config = True
            request_user.save()
        else:
            request_user.config = False
            request_user.save()