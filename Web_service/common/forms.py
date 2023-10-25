from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserInfo
from django.contrib.auth.hashers import check_password

# 사용자 생성
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ('user_id', 'gender', 'birth_date', 'address')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# 정보 변경
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserInfo
        fields = ('user_id', 'password', 'gender', 'birth_date', 'address',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

# 일반 유저 정보 변경
class NormalUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = UserInfo
        fields = ['user_id', 'gender', 'birth_date', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.birth_date:
            self.initial['birth_date'] = self.instance.birth_date.strftime('%Y-%m-%d')

        if self.instance and self.instance.gender:
            self.initial['gender'] = self.instance.gender
            
# 로그인
class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = UserInfo
        fields = ('user_id', 'password') # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.


# 회원탈퇴 
class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control',}), 
    )
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
