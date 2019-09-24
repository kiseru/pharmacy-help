from django.conf.urls import url
from django.urls import path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from recipes import views
from recipes.views import *

router = routers.DefaultRouter()
router.register('login', views.LoginViewSet)
router.register('recipes', views.RecipesViewSet)
router.register('users', views.UserViewSet)

old_urls = [
    path('', get_swagger_view()),
    url('^medicines/edit/(?P<id>\d+)$', edit_medicine, name='edit_medicine'),
    url('^search/medicine/', SearchMedicineViewSet.as_view({'get': 'list'})),
    url('^search/medicine_type/', SearchMedicineTypesViewSet.as_view({'get': 'list'})),
    url('^medicine_pharmacy/', MedicineWithPharmaciesViewSet.as_view({'get': 'list'})),
    url('^pharmacies', find_pharmacies),
    url('^workers/(?P<pk>\d+)/delete', WorkerViewSet.as_view({'post': 'destroy'})),
    url('^workers/(?P<pk>\d+)$', WorkerViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url('^workers/new$', WorkerViewSet.as_view({'post': 'create'})),
    url('^workers/$', WorkerViewSet.as_view({'get': 'list'})),
    url('^medicines/$', GoodsViewSet.as_view({'get': 'list'})),
    url('^medicines/new', GoodsViewSet.as_view({'post': 'create'})),
    url('^medicines/(?P<pk>\d+)', GoodsViewSet.as_view({'get': 'retrieve', 'post': 'update'})),
]

urlpatterns = old_urls + router.urls
