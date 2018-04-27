import rest_framework
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions, mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from recipes.auth import login_not_required, has_role, get_default_url, get_role
from recipes.forms import UserForm, LoginForm, MedicineNamesForm, MedicineTypeForm, MedicineForm
from recipes.models import Recipe
from recipes.serializers import serialize_user, RecipeShortSerializer, UserSerializer, RecipeFullSerializer
from recipes.services import get_recipes, get_recipes_of_doctor, create_recipe


import json
import traceback


def response_to_api_format(func):
    def new_func(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
            if status.is_success(response.status_code):
                new_response = {
                  'status': 'success',
                  'data': response.data,
                  'error': None
                }
                response.data = new_response
            elif status.is_client_error(response.status_code):
                new_response = {
                  'status': 'fail',
                  'data': response.data,
                  'error': 'invalid_data'
                }
                response.data = new_response
            return response
        except (rest_framework.exceptions.ValidationError, ValidationError, ObjectDoesNotExist):
            traceback.print_exc()
            new_response = {
                'status': 'fail',
                'data': None,
                'error': 'invalid_data'
            }
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            traceback.print_exc()
            new_response = {
              'status': 'fail',
              'error': str(e),
              'data': None,
            }
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)
    return new_func


@login_required(login_url=reverse_lazy('home'))
def user_info(request):
    errors = []
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            errors = json.loads(form.errors.as_json())
            errors = errors if isinstance(errors, list) else [errors, ]
    return JsonResponse(serialize_user(request.user, errors))


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


@login_required(login_url=reverse_lazy('home'))
def profile(request):
    return render(request, 'index.html')


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@method_decorator(has_role('doctor'), name='create')
@method_decorator(response_to_api_format, name='create')
class RecipeCreationViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
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


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
class TemplateViewForAuthenticated(TemplateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(has_role('apothecary'), name='dispatch')
class TemplateViewForApothecary(TemplateView):
    pass


@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(has_role('doctor'), name='dispatch')
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
