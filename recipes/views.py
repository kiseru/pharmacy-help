import traceback
from uuid import uuid4

import rest_framework
from django import http
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import *
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import status, permissions, mixins, viewsets, authentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes, action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from recipes import services, serializers, models
from recipes.auth import \
    AdminPermission, ApothecaryPermission
from recipes.exceptions import AlreadyExistsException
from recipes.models import Recipe, MedicineName, MedicineType, MedicinesPharmacies, Medicine, User
from recipes.permissions import IsDoctor
from recipes.serializers import UserSerializer, MedicineNameSerializer, MedicineTypeSerializer, \
    MedicineWithPharmaciesSerializer, GoodSerializer
from recipes.services import get_pharmacies_and_medicines, add_worker, update_user, get_workers, \
    delete_worker


def response_to_api_format(func):
    def new_func(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
            if response.__class__ != Response:
                return response
            if status.is_success(response.status_code) or status.is_redirect(response.status_code):
                response.data = get_response(is_success=True, data=response.data)
            elif status.is_client_error(response.status_code):
                response.data = get_response(is_success=False, data=response.data, error='invalid_data')
            return response
        except (rest_framework.exceptions.ValidationError, ValidationError, ObjectDoesNotExist, ValueError):
            traceback.print_exc()
            new_response = get_response(is_success=False, error='invalid_data')
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)
        except http.response.Http404:
            traceback.print_exc()
            new_response = get_response(is_success=False, error='not_found')
            return Response(data=new_response, status=status.HTTP_404_NOT_FOUND)
        except AlreadyExistsException:
            new_response = get_response(is_success=False, error='already_exists')
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            new_response = get_response(is_success=False, error=str(e))
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)

    return new_func


def get_response(is_success, error=None, data=None):
    return {
        'status': 'success' if is_success else 'fail',
        'error': error,
        'data': data,
    }


class LoginViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.none()
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if user is None or not user.check_password(serializer.validated_data['password']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user_id=user.id)
        return Response({'token': token.key, 'role': user.role})


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)


def edit_medicine(request, id):
    try:
        medicine = MedicinesPharmacies.objects.get(id=id)
        if request.method == "POST":
            medicine.medicine.medicine_name.medicine_name = request.POST.get("name")
            medicine.medicine.medicine_type.type_name = request.POST.get("type_name")
            medicine.medicine.medicine_name.medicine_description = request.POST.get("description")
            medicine.count = request.POST.get("count")
            medicine.price = request.POST.get("price")
            medicine.medicine.medicine_name.save()
            medicine.medicine.medicine_type.save()
            medicine.save()
            return HttpResponseRedirect("/api/medicines/")
        else:
            return render(request, "recipes/edit_medicine.html", {"medicine": medicine})
    except MedicinesPharmacies.DoesNotExist:
        return HttpResponseNotFound("<h2>Medicine not found</h2>")


class RecipesViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.none()
    permission_classes = (permissions.IsAuthenticated,
                          IsDoctor)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor, token=uuid4())

    def get_queryset(self):
        return Recipe.objects.filter(doctor__user=self.request.user)


class SearchMedicineViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = MedicineName.objects.all()
    serializer_class = MedicineNameSerializer

    def list(self, request, *args, **kwargs):
        if 'medicine_name' in request.GET:
            self.queryset = self.queryset.filter(medicine_name__icontains=request.GET['medicine_name'])
        return super().list(request, *args, *kwargs)


class SearchMedicineTypesViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = MedicineType.objects.all()
    serializer_class = MedicineTypeSerializer

    def list(self, request, *args, **kwargs):
        if 'type_name' in request.GET:
            self.queryset = self.queryset.filter(type_name__icontains=request.GET['type_name'])
        return super().list(request, *args, *kwargs)


class MedicineWithPharmaciesViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = None
    serializer_class = MedicineWithPharmaciesSerializer

    def list(self, request, *args, **kwargs):
        if 'id' in request.GET:
            self.queryset = Medicine.objects.filter(medicine_name__pk=request.GET['id'])
        else:
            self.queryset = Medicine.objects.all()
        return super().list(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes((SessionAuthentication,))
@renderer_classes((JSONRenderer,))
def find_pharmacies(request):
    try:
        data = {
            'medicines': request.GET.getlist('medicines'),
            'city_name': request.GET['city_name'],
            'coordinates': (float(request.GET['latitude']), float(request.GET['longitude'])) if ('latitude'
                                                                                                 and 'longitude'
                                                                                                 in request.GET) else None,
        }
        result = get_pharmacies_and_medicines(data)
        return Response(result)
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(response_to_api_format, name='create')
@method_decorator(response_to_api_format, name='update')
class WorkerViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (AdminPermission,)

    def list(self, request, *args, **kwargs):
        self.queryset = get_workers(request.user, request.GET['query'] if 'query' in request.GET else None)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        user = add_worker(user_serializer=serializer, admin=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(data={'id': user.id}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        update_user(serializer, instance)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_worker(instance)
        return Response(status=status.HTTP_200_OK)


@method_decorator(response_to_api_format, name='create')
@method_decorator(response_to_api_format, name='update')
class GoodsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    renderer_classes = (JSONRenderer,)
    queryset = None
    serializer_class = GoodSerializer
    permission_classes = (ApothecaryPermission,)

    def list(self, request, *args, **kwargs):
        pharmacy = request.user.apothecary_set.all()[0].pharmacy
        self.queryset = pharmacy.medicinespharmacies_set.all()
        if 'name_id' in request.GET:
            self.queryset = self.queryset.filter(medicine__medicine_name__id=request.GET['name_id'])
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        good = services.add_medicine(data, request.user)
        return Response(data={'id': good.id}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        pharmacy = request.user.apothecary_set.all()[0].pharmacy
        self.queryset = pharmacy.medicinespharmacies_set.all()
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pharmacy = request.user.apothecary_set.all()[0].pharmacy
        self.queryset = pharmacy.medicinespharmacies_set.all()
        instance = self.get_object()
        data = request.data
        services.update_medicine(instance, data)
        return Response(status=status.HTTP_200_OK)


class MedicineViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    def get_queryset(self):
        pharmacy = self.request.user.apothecary_set.first()
        return pharmacy.medicinespharmacies_set.all()
