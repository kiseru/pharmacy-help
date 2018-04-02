from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.
from recipes.forms import LoginForm, UserForm
from recipes.serializers import serialize_user
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
    return JsonResponse(serialize_user(request.user, errors))


@login_required(login_url=reverse_lazy('login'))
def test_user_info(request):
    return render(request, 'recipes/test_user_info.html', {'form': UserForm(instance=request.user)})


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
                return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        # return render(request, 'recipes/login.html', {'form': LoginForm})
        return render(request, 'recipes/index.html')


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'recipes/index.html')


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))