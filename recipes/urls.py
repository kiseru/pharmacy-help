from django.conf.urls import url

from recipes.views import *

urlpatterns = [
    url(r'user$', user_info, name='user_info')
]