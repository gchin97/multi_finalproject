from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import logout as auth_logout
from .forms import UserCreationForm, NormalUserChangeForm, CheckPasswordForm

# Create your views here.
# 회원가입
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

# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('prediction:index')

# 회원탈퇴
def delete(request):
    user = request.user
    user.delete()
    auth_logout(request)
    return redirect('prediction:index')

# 회원정보 수정
def update(request):
    if request.method == 'POST':
        form = NormalUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('prediction:main')
    else:
        form = NormalUserChangeForm(instance=request.user)
    context = {'form':form}
    return render(request, 'common/update.html', context)

# 비밀번호 변경
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully changed')
            return render(request, 'prediction/main.html')
        else:
            messages.error(request, 'Password not changed')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'common/update.html',{'form':form})

# 회원탈퇴 
#login_message_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            return redirect('/common/login/')
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'common/profile_delete.html', {'password_form':password_form})
