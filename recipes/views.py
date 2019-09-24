import json
import traceback

import rest_framework
from django import http
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import *
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import status, permissions, mixins, viewsets, authentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes, action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from recipes import services, serializers, models
from recipes.auth import has_role, has_role_for_template_view, \
    AdminPermission, ApothecaryPermission, is_admin_for_template_view
from recipes.exceptions import AlreadyExistsException
from recipes.forms import UserForm, MedicineNamesForm, MedicineTypeForm, MedicineForm, MedicinePharmacyForm
from recipes.models import Recipe, MedicineName, MedicineType, MedicinesPharmacies, Medicine, User
from recipes.serializers import RecipeShortSerializer, UserSerializer, RecipeFullSerializer, \
    MedicineNameSerializer, MedicineTypeSerializer, MedicineWithPharmaciesSerializer, GoodSerializer, \
    MedicineRequestSerializerForUpdate
from recipes.services import get_recipes, get_recipes_of_doctor, create_recipe
from recipes.services import serve_recipe, get_pharmacies_and_medicines, add_worker, update_user, get_workers, \
    delete_worker, get_recipe_with_goods


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


@login_required(login_url=reverse_lazy('home'))
def test_user_info(request):
    return render(request, 'recipes/test_user_info.html', {'form': UserForm(instance=request.user)})


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


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@method_decorator(has_role('doctor'), name='create')
@method_decorator(has_role('apothecary'), name='update')
@method_decorator(response_to_api_format, name='create')
@method_decorator(response_to_api_format, name='update')
class RecipeCreationViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = Recipe.objects.all()
    serializer_class = RecipeFullSerializer

    lookup_field = 'token'

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        recipe = Recipe(**serializer.data, doctor=request.user.doctor_set.all()[0])
        create_recipe(recipe, data, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        requests = MedicineRequestSerializerForUpdate(data=request.data['requests'], many=True)
        print(requests.initial_data)
        serve_recipe(requests.initial_data, instance, request.user.apothecary_set.first())
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((ApothecaryPermission,))
@renderer_classes((JSONRenderer,))
def get_recipe_for_apothecary(request, token):
    instance = Recipe.objects.get(token=token)
    serializer = RecipeFullSerializer(instance=instance)
    return Response(get_recipe_with_goods(serializer.data, request), status=status.HTTP_200_OK)


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
class TemplateViewForAuthenticated(TemplateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(is_admin_for_template_view, name='dispatch')
class TemplateViewForAdmins(TemplateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(has_role_for_template_view('apothecary'), name='dispatch')
class TemplateViewForApothecary(TemplateView):
    pass


class TemplateViewForDoctor(TemplateView):
    pass


def index(request):
    medicines = MedicinesPharmacies.objects.all()
    return render(request, 'recipes/medicines.html', {"medicines": medicines})


def add_medicine(request):
    ctx = {
        'medicine_name_form': MedicineNamesForm(),
        'medicine_type_form': MedicineTypeForm(),
        'medicine_form': MedicineForm(),
        'medicine_pharmacy_form': MedicinePharmacyForm()}
    if request.method == 'POST':
        ctx['medicine_name_form'] = MedicineNamesForm(request.POST)
        ctx['medicine_type_form'] = MedicineTypeForm(request.POST)
        ctx['medicine_form'] = MedicineForm(request.POST)
        ctx['medicine_pharmacy_form'] = MedicinePharmacyForm(request.POST)
        if (ctx['medicine_name_form'].is_valid()) and (ctx['medicine_type_form'].is_valid()) and \
            (ctx['medicine_form'].is_valid()) and (ctx['medicine_pharmacy_form'].is_valid()):
            instance_medicine_name = ctx['medicine_name_form'].save()
            instance_medicine_type = ctx['medicine_type_form'].save()
            instance_medicine_pharmacy = ctx['medicine_pharmacy_form']
            instance = ctx['medicine_form'].save(request, m1=instance_medicine_type,
                                                 m2=instance_medicine_name, m3=instance_medicine_pharmacy)
            instance.save()
            return redirect('/api/medicines/')
    return render(request, 'recipes/add_medicine.html', ctx)


def get_medicine(request):
    pharmacy = request.user.apothecary_set.all()[0].pharmacy
    medicinepharmacies = pharmacy.medicinespharmacies_set.all()
    if 'name_id' in request.GET:
        medicinepharmacies = medicinepharmacies.filter(medicine__medicine_name__id=request.GET['name_id'])
    return HttpResponse(
        json.dumps([get_medicine_json(i) for i in medicinepharmacies], ensure_ascii=False),
        content_type='application/json'
    )


def get_medicine_json(medicinepharmacy):
    return {
        'price': medicinepharmacy.price,
        'count': medicinepharmacy.count,
        'id': medicinepharmacy.id,
        'description': medicinepharmacy.medicine.medicine_name.medicine_description,
        'name': medicinepharmacy.medicine.medicine_name.medicine_name,
        'type': medicinepharmacy.medicine.medicine_type.type_name,
    }


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


@method_decorator(response_to_api_format, name='post')
class UserInfoView(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(instance=request.user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data.update({"error": serializer.errors}), status=status.HTTP_400_BAD_REQUEST)


class RecipesViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = None
    serializer_class = RecipeShortSerializer

    def list(self, request, *args, **kwargs):
        token = request.GET['id'] if 'id' in request.GET else ''
        if request.user.role is 'doctor':
            self.queryset = get_recipes_of_doctor(request.user.doctor_set.first(), token).order_by('-date')[:10]
        else:
            self.queryset = get_recipes(token).order_by('-date')[:10]
        return super().list(request, *args, **kwargs)


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
