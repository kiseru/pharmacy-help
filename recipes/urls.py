from django.conf.urls import url
from django.views.generic import TemplateView

from recipes.views import *

urlpatterns = [
    url('', do_login, name='login'),
    url('logout/', do_logout, name='logout'),
    url('api/user/', user_info, name='user_info'),
    url('api/test_user_info/', test_user_info, name='test_user_info'),
    url('api/recipes/', RecipesListJsonView.as_view(), name='recipes'),
    url('medicine/', TemplateView.as_view(template_name='recipes/index.html')),
    url('medicine/add/', TemplateView.as_view(template_name='recipes/index.html')),
    url('recipes/<str:token>', TemplateView.as_view(template_name='recipes/index.html')),
    url('recipes/', TemplateView.as_view(template_name='recipes/index.html')),
    url('apothecary/', TemplateView.as_view(template_name='recipes/index.html')),
    url('doctor/', TemplateView.as_view(template_name='recipes/index.html')),
]

