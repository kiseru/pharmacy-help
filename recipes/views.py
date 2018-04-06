from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

# Create your views here.
from recipes.auth import login_not_required, has_role
from recipes.forms import LoginForm


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
                return HttpResponseRedirect(reverse('profile'))
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'recipes/login.html', {'form': LoginForm})


@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return HttpResponse('My page')


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))