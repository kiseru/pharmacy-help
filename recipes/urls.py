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
    url('^api/user/', UserInfoView.as_view(), name='user_info'),
    url('^api/test_user_info/', test_user_info, name='test_user_info'),
    url('^api/recipes/$', RecipesViewSet.as_view({'get': 'list'}), name='recipes'),
    url('^api/recipes/new$', RecipeCreationViewSet.as_view({ 'post': 'create'}), name='add_recipe'),
    url('^api/recipes/create$', TemplateViewForAuthenticated.as_view(template_name='recipe.html')),
    url('^api/recipes/(?P<token>.+)$', RecipeCreationViewSet.as_view({'get': 'retrieve', 'post': 'update'}), name='recipe'),
    url('^api/login', do_login_ajax, name='login_ajax'),
    url('^api/test_serving_recipe', TemplateView.as_view(template_name='recipes/test_serving_recipe.html')),
    url('^apothecary/medicines/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/medicines/new$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/recipes/', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/recipes/', TemplateViewForDoctor.as_view(template_name='index.html')),
    url('^apothecary/workers/', TemplateViewForAdmins.as_view(template_name='index.html')),
    url('^doctor/workers/', TemplateViewForAdmins.as_view(template_name='index.html')),
    url('^apothecary/new', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/(?P<token>.+)/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/$', TemplateViewForDoctor.as_view(template_name='index.html')),
    # url('^api/medicines/new/', add_medicine, name='add_medicine'),
    # url('^api/medicines', get_medicine, name='medicine'),
    url('^api/search/medicine/', SearchMedicineViewSet.as_view({'get': 'list'})),
    url('^api/search/medicine_type/', SearchMedicineTypesViewSet.as_view({'get': 'list'})),
    url('^api/medicine_pharmacy/', MedicineWithPharmaciesViewSet.as_view({'get': 'list'})),
    url('^api/pharmacies', find_pharmacies),
    url('^api/workers/(?P<pk>\d+)', WorkerViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url('^api/workers/new$', WorkerViewSet.as_view({'post': 'create'})),
    url('^api/workers/$', WorkerViewSet.as_view({'get': 'list'})),
    url('^patient/recipe/(?P<token>.+)', TemplateView.as_view(template_name='index.html'), name='show_recipe'),
    url('^api/medicines/$', GoodsViewSet.as_view({'get': 'list'})),
    url('^api/medicines/new', GoodsViewSet.as_view({'post': 'create'})),
    url('^api/medicines/(?P<pk>\d+)', GoodsViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
    # url(r'^api/', include(router.urls)),
]

