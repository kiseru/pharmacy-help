from django.conf.urls import url
from django.views.generic import TemplateView

from recipes.views import *

urlpatterns = [
    url('^$', do_login, name='home'),
    url('^login$', do_login, name='login'),
    url('^logout/', do_logout, name='logout'),
    url('^api/login', do_login_ajax, name='login_ajax'),
    url('^api/user/', user_info, name='user_info'),
    url('^api/test_user_info/', test_user_info, name='test_user_info'),
    url('^api/recipes/$', get_recipes_view, name='recipes'),
    url('^api/recipes/new$', add_recipe, name='add_recipe'),
    url('^medicines/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^medicines/new$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^recipes/(?P<token>.+)', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^recipes/$', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^api/recipes/create$', TemplateViewForAuthenticated.as_view(template_name='recipe.html')),
    url('^apothecary/', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/', TemplateViewForDoctor.as_view(template_name='index.html')),
    url('^api/medicines/new/', add_medicine, name='add_medicine'),
    url('^api/medicines', get_medicine, name='medicine')
]

