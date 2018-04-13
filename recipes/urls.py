from django.conf.urls import url
from django.views.generic import TemplateView

from recipes.views import *

urlpatterns = [
    url('^$', do_login, name='home'),
    url('^login$', do_login, name='login'),
    url('^logout/', do_logout, name='logout'),
    url('^api/user/', user_info, name='user_info'),
    url('^api/test_user_info/', test_user_info, name='test_user_info'),
    url('^api/recipes/', RecipesListJsonView.as_view(), name='recipes'),
    url('^medicines/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^medicines/new$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^recipes/(?P<token>.+)', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^recipes/$', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^apothecary/', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/', TemplateViewForDoctor.as_view(template_name='index.html')),
]

