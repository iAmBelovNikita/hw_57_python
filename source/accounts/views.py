from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, LoginForm

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get('next') or request.POST.get('next') or 'project-list'
            return redirect(next_url)
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = MyUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.POST.get('next') or 'project-list'
            return redirect(next_url)
    else:
        form = MyUserCreationForm()
    return render(request, 'accounts/register.html', context={'form': form})