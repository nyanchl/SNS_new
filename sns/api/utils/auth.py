import time
import jwt
from sns.settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from api.models import UserInfo

# class CustomAuthentication(BaseAuthentication):