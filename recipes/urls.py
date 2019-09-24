from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from recipes import views
from recipes.views import *

router = routers.DefaultRouter()
router.register('goods', views.GoodsViewSet)
router.register('login', views.LoginViewSet)
router.register('medicines', views.MedicineViewSet)
router.register('recipes', views.RecipesViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url('^search/medicine/', SearchMedicineViewSet.as_view({'get': 'list'})),
    url('^search/medicine_type/', SearchMedicineTypesViewSet.as_view({'get': 'list'})),
    url('^medicine_pharmacy/', MedicineWithPharmaciesViewSet.as_view({'get': 'list'})),
    url('^pharmacies', find_pharmacies),
    url('^workers/(?P<pk>\d+)/delete', WorkerViewSet.as_view({'post': 'destroy'})),
    url('^workers/(?P<pk>\d+)$', WorkerViewSet.as_view({'post': 'update', 'get': 'retrieve'})),
    url('^workers/new$', WorkerViewSet.as_view({'post': 'create'})),
    url('^workers/$', WorkerViewSet.as_view({'get': 'list'})),
]
