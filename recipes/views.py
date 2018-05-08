import rest_framework
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from recipes.auth import login_not_required, has_role, get_default_url, get_role, has_role_for_template_view
from recipes.forms import UserForm, MedicineNamesForm, MedicineTypeForm, MedicineForm
from recipes.models import Recipe, MedicineName, MedicineType
from recipes.serializers import serialize_user, RecipeShortSerializer, UserSerializer, RecipeFullSerializer, \
  MedicineNameSerializer, MedicineTypeSerializer
from recipes.services import serve_recipe
from recipes.services import get_recipes, get_recipes_of_doctor, create_recipe

import json
import traceback


def response_to_api_format(func):
    def new_func(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
            if response.__class__ != Response:
                return response
            if status.is_success(response.status_code):
                response.data = get_response(is_success=True, data=response.data)
            elif status.is_client_error(response.status_code):
                response.data = get_response(is_success=False, data=response.data, error='invalid_data')
            return response
        except (rest_framework.exceptions.ValidationError, ValidationError, ObjectDoesNotExist):
            traceback.print_exc()
            new_response = get_response(is_success=False, error='invalid_data')
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


@login_not_required()
def do_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponseRedirect(get_default_url(get_role(user)))
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        # return render(request, 'recipes/login.html', {'form': LoginForm})
        return render(request, 'index.html')


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
@authentication_classes((SessionAuthentication,))
@renderer_classes((JSONRenderer,))
@response_to_api_format
def do_login_ajax(request):
    print(request)
    if request.method == 'POST':
        print(request.is_ajax())
        # json_str = list(request.POST.dict().keys())[0]
        data = request.data
        if 'email' in data and 'password' in data:
            user = authenticate(username=data['email'], password=data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                raise Exception('not_found')
        else:
            raise Exception('invalid_data')
    else:
        return render(request, 'recipes/test_login.html')
  

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@method_decorator(has_role('doctor'), name='create')
@method_decorator(has_role('apothecary'), name='update')
@method_decorator(response_to_api_format, name='create')
@method_decorator(response_to_api_format, name='update')
@method_decorator(response_to_api_format, name='retrieve')
class RecipeCreationViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            GenericViewSet):
    renderer_classes = (JSONRenderer,)
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeFullSerializer
    
    lookup_field = 'token'
    
    def create(self, request, *args, **kwargs):
        json_str = list(request.POST.dict().keys())[0]
        data = json.loads(json_str)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        print(serializer.is_valid())
        # self.perform_create(serializer)
        recipe = Recipe(**serializer.data, doctor=request.user.doctor_set.all()[0])
        create_recipe(recipe, data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        json_str = list(request.POST.dict().keys())[0]
        medicines = json.loads(json_str)
        print(medicines)
        serve_recipe(medicines, instance, request.user.apothecary_set.all()[0])
        return Response(status=status.HTTP_200_OK)


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
class TemplateViewForAuthenticated(TemplateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(has_role_for_template_view('apothecary'), name='dispatch')
class TemplateViewForApothecary(TemplateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(has_role_for_template_view('doctor'), name='dispatch')
class TemplateViewForDoctor(TemplateView):
    pass


def add_medicine(request):
    ctx = {
         'medicine_name_form': MedicineNamesForm(),
         'medicine_type_form': MedicineTypeForm(),
         'medicine_form': MedicineForm()}
    if request.method == 'POST':
        ctx['medicine_name_form'] = MedicineNamesForm(request.POST)
        ctx['medicine_type_form'] = MedicineTypeForm(request.POST)
        ctx['medicine_form'] = MedicineForm(request.POST)
        if (ctx['medicine_name_form'].is_valid()) and (ctx['medicine_type_form'].is_valid()) and (ctx['medicine_form'].is_valid()):
            instance_medicine_name = ctx['medicine_name_form'].save()
            instance_medicine_type = ctx['medicine_type_form'].save()
            instance = ctx['medicine_form'].save(m1=instance_medicine_type, m2=instance_medicine_name)
            instance.save()
            return redirect('medicine')
    return render(request, 'recipes/add_medicine.html', ctx)

# def get_medicine(request):
#     medicines = Medicines_pharmacies.objects.values('medicine_id',
#                                                     'medicine_id__medicine_name_id__medicine_name',
#                                                     'medicine_id__medicine_name_id__description',
#                                                     'medicine_id__medicine_type_id__type_name',
#                                                     'medicine_id__medicines_pharmacies__count',
#                                                     'medicine_id__medicines_pharmacies__price',)
#     return JsonResponse({'medicines': list(medicines)})


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


@method_decorator(response_to_api_format, name='post')
class UserInfoView(APIView):
    renderer_classes = (JSONRenderer,)
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        data = request.POST
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
            self.queryset = get_recipes_of_doctor(request.user.doctor_set.all()[0], token).order_by('-date')[:10]
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
