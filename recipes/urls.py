from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from recipes import views
from recipes.views import *

router = routers.DefaultRouter()
router.register('apothecaries', views.ApothecaryViewSet)
router.register('goods', views.GoodsViewSet)
router.register('login', views.LoginViewSet)
router.register('medicines', views.MedicineViewSet)
router.register('medicines_with_pharmacies', views.MedicineWithPharmaciesViewSet)
router.register('recipes', views.RecipesViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url('^pharmacies', find_pharmacies),
]
