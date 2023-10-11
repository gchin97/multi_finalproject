from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout
from .forms import UserCreationForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('user_id')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('prediction:main')
    else:
        form = UserCreationForm()
    return render(request, 'common/signup.html', {'form':form})

def login(request):
    if request.method == 'POST':
        # 로그인 처리
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('prediction:main')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'common/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('prediction:index')