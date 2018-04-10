from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import BaseListView

from recipes.auth import login_not_required, has_role, get_default_url, get_role
from recipes.forms import UserForm, LoginForm
from recipes.models import Recipe
from recipes.serializers import serialize_user, JsonSerializer, RecipeSerializerShort
from recipes.services import get_recipes

import json


@login_required(login_url=reverse_lazy('login'))
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


@login_required(login_url=reverse_lazy('login'))
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
            return HttpResponseRedirect(reverse('login'))
    else:
        # return render(request, 'recipes/login.html', {'form': LoginForm})
        return render(request, 'index.html')


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'index.html')


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


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


@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
@method_decorator(has_role('apothecary'), name='dispatch')
class RecipesListJsonView(ListJsonView):
    paginate_by = 10
    model = Recipe
    ordering = '-date'
    serializer = RecipeSerializerShort

    def filter_query_set(self, query):
        return get_recipes(query)

