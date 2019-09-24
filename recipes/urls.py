from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from recipes import views
from recipes.views import *

router = routers.DefaultRouter()
router.register('api/login', views.LoginViewSet)
router.register('api/recipes', views.RecipesViewSet)
router.register('api/users', views.UserViewSet)

old_urls = [
    path('', get_swagger_view()),
    url('^api/medicines/edit/(?P<id>\d+)$', edit_medicine, name='edit_medicine'),
    url('^api/recipes/create$', TemplateViewForAuthenticated.as_view(template_name='recipe.html')),
    url('^api/recipes/(?P<token>[0-9a-zA-Z]+)$',
        RecipeCreationViewSet.as_view({'post': 'update', 'get': 'retrieve'}), name='recipe'),
    url('^api/recipes/(?P<token>[0-9a-zA-Z]+)/confirm$', get_recipe_for_apothecary),
    url('^api/test_serving_recipe',
        TemplateView.as_view(template_name='recipes/test_serving_recipe.html')),
    url('^apothecary/medicines/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/medicines/new$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/recipes/', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/recipes/', TemplateViewForDoctor.as_view(template_name='index.html')),
    url('^apothecary/workers/', TemplateViewForAdmins.as_view(template_name='index.html')),
    url('^doctor/workers/', TemplateViewForAdmins.as_view(template_name='index.html')),
    url('^workers/', TemplateViewForAdmins.as_view(template_name='index.html')),
    url('^recipes/', TemplateViewForAuthenticated.as_view(template_name='index.html')),
    url('^apothecary/new', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/(?P<token>.+)$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^apothecary/$', TemplateViewForApothecary.as_view(template_name='index.html')),
    url('^doctor/$', TemplateViewForDoctor.as_view(template_name='index.html')),
    url('^api/search/medicine/', SearchMedicineViewSet.as_view({'get': 'list'})),
    url('^api/search/medicine_type/', SearchMedicineTypesViewSet.as_view({'get': 'list'})),
    url('^api/medicine_pharmacy/', MedicineWithPharmaciesViewSet.as_view({'get': 'list'})),
    url('^api/pharmacies', find_pharmacies),
    url('^api/workers/(?P<pk>\d+)/delete', WorkerViewSet.as_view({'post': 'destroy'})),
    url('^api/workers/(?P<pk>\d+)$', WorkerViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url('^api/workers/new$', WorkerViewSet.as_view({'post': 'create'})),
    url('^api/workers/$', WorkerViewSet.as_view({'get': 'list'})),
    url('^patient/recipe/(?P<token>.+)', TemplateView.as_view(template_name='index.html'),
        name='show_recipe'),
    url('^api/medicines/$', GoodsViewSet.as_view({'get': 'list'})),
    url('^api/medicines/new', GoodsViewSet.as_view({'post': 'create'})),
    url('^api/medicines/(?P<pk>\d+)', GoodsViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
]

urlpatterns = old_urls + router.urls
