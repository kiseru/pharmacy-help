from django.conf.urls import url
from django.urls import include
from django.views.generic import TemplateView
from rest_framework import routers

from recipes.views import *

# router = routers.DefaultRouter()
# router.register(r'recipe/', RecipeCreationViewSet, base_name='recipe')

urlpatterns = [
    url('^$', do_login, name='home'),
    url('^login$', do_login, name='login'),
    url('^logout/', do_logout, name='logout'),
    # url('^api/user/', user_info, name='user_info'),
    url('^api/user/', UserInfoView.as_view(), name='user_info'),
    url('^api/test_user_info/', test_user_info, name='test_user_info'),
    # url('^api/recipes/$', get_recipes_view, name='recipes'),
    url('^api/recipes/$', RecipesViewSet.as_view({'get': 'list'}), name='recipes'),
    # url('^api/recipes/new$', add_recipe, name='add_recipe'),
    url('^api/recipes/new$', RecipeCreationViewSet.as_view({ 'post': 'create'}), name='add_recipe'),
    url('^api/recipes/create$', TemplateViewForAuthenticated.as_view(template_name='recipe.html')),
    url('^api/recipes/(?P<token>.+)$', RecipeCreationViewSet.as_view({'get': 'retrieve'}), name='recipe'),
    url('^medicines/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^medicines/new$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^recipes/(?P<token>.+)', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^recipes/$', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^apothecary/', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/', TemplateViewForDoctor.as_view(template_name='index.html')),
    url('^api/medicines/new/', add_medicine, name='add_medicine'),
    url('^api/medicines', get_medicine, name='medicine'),
    # url(r'^api/', include(router.urls)),
]

