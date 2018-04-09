from django.conf.urls import url
from django.views.generic import TemplateView

from recipes.views import *

urlpatterns = [
    url(r'^logout$', do_logout, name='logout'),
    url(r'^api/user$', user_info, name='user_info'),
    url(r'^api/test_user_info', test_user_info, name='test_user_info'),
    url(r'^medicine$', TemplateView.as_view(template_name='recipes/index.html')),
    url(r'^medicine/add$', TemplateView.as_view(template_name='recipes/index.html')),
    url(r'^recipe$', TemplateView.as_view(template_name='recipes/index.html')),
    url(r'^recipes$', TemplateView.as_view(template_name='recipes/index.html')),
    url(r'^$', do_login, name='login'),
]
