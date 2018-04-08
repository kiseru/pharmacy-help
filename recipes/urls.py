from django.conf.urls import url

from recipes.views import *

urlpatterns = [
    url(r'user$', user_info, name='user_info'),
    url(r'test_user_info', test_user_info, name='test_user_info'),
    url(r'recipes', RecipesListJsonView.as_view(), name='recipes')
]
