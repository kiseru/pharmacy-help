from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import BaseListView

from recipes.auth import login_not_required, has_role, get_default_url, get_role
from recipes.forms import UserForm, LoginForm, MedicineNamesForm, MedicineTypeForm, MedicineForm
from recipes.models import Recipe
from recipes.serializers import serialize_user, JsonSerializer, RecipeSerializerShort
from recipes.services import get_recipes

import json


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


# нафиг пока не надо
class ListJsonView(BaseListView):
    query_param = 'query'
    serializer = JsonSerializer

    def get_json(self, object):
        return self.serializer.get_json(object)

    def filter_query_set(self, query):
        return self.queryset

    def get(self, request, *args, **kwargs):
        if self.query_param:
            if self.query_param in request.GET:
                query_param_value = request.GET[self.query_param]
            else:
                query_param_value = None
            self.queryset = self.filter_query_set(query_param_value)
            paginator, page, queryset, is_paginated = self.paginate_queryset(self.queryset, self.paginate_by)
            data = [self.get_json(i) for i in queryset]
            result = {
                'has_prev': page.has_previous(),
                'has_next': page.has_next(),
                'object_list': data,
                'page_number': paginator.num_pages,
            }
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')
        else:
            raise Exception("Field 'query_param' should be defined")


# и это не надо
@method_decorator(login_required(login_url=reverse_lazy('home')), name='dispatch')
@method_decorator(has_role('apothecary'), name='dispatch')
class RecipesListJsonView(ListJsonView):
    paginate_by = 10
    model = Recipe
    ordering = '-date'
    serializer = RecipeSerializerShort

    def filter_query_set(self, query):
        return get_recipes(query)



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


@login_required(login_url=reverse_lazy('home'))
@has_role('apothecary')
def get_recipes_view(request):
    token = request.GET['id'] if 'id' in request.GET else ''
    queryset = get_recipes(token).order_by('-date')[:10]
    result = [RecipeSerializerShort.get_json(i) for i in queryset]
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json')


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
