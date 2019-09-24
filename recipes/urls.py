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
    url('^api/recipes/(?P<token>[0-9a-zA-Z]+)/confirm$', get_recipe_for_apothecary),
    url('^api/search/medicine/', SearchMedicineViewSet.as_view({'get': 'list'})),
    url('^api/search/medicine_type/', SearchMedicineTypesViewSet.as_view({'get': 'list'})),
    url('^api/medicine_pharmacy/', MedicineWithPharmaciesViewSet.as_view({'get': 'list'})),
    url('^api/pharmacies', find_pharmacies),
    url('^api/workers/(?P<pk>\d+)/delete', WorkerViewSet.as_view({'post': 'destroy'})),
    url('^api/workers/(?P<pk>\d+)$', WorkerViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url('^api/workers/new$', WorkerViewSet.as_view({'post': 'create'})),
    url('^api/workers/$', WorkerViewSet.as_view({'get': 'list'})),
    url('^api/medicines/$', GoodsViewSet.as_view({'get': 'list'})),
    url('^api/medicines/new', GoodsViewSet.as_view({'post': 'create'})),
    url('^api/medicines/(?P<pk>\d+)', GoodsViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
]

urlpatterns = old_urls + router.urls
