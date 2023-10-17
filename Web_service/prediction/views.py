from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import EmpPredictionForm
from .models import *
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    return render(request, 'prediction/index.html')

def main(request):
    user_id = request.user.user_id
    username = user_id.split('@')[0] # 메인페이지 이메일 형식 슬라이싱 추가
    return render(request, 'prediction/main.html', {'username': username}) # username을 호출하는 경우 슬라이싱 된 아이디만 반환

def predict(request):
    if request.method == 'POST':
        form = EmpPredictionForm(request.POST)
        if form.is_valid():
            predict = form.save(commit=False)
            result = 1
            return render(request, 'prediction/predict.html', {'result':result})
    else:
        form = EmpPredictionForm()
    result = 0
    context = {'form':form}
    return render(request, 'prediction/predict.html', context)

def emp(request):
    city_list = EmpInfo.objects.values_list('city', flat=True).distinct()
    job_list = EmpInfo.objects.values_list('job_name', flat=True).distinct()

    if request.method == 'POST':
        # 필터링을 적용한 경우
        selected_cities = request.POST.getlist("city")
        selected_jobs = request.POST.getlist("job_name")

        emp_list = EmpInfo.objects.all().values('city', 'job_name', 'company').distinct()

        if selected_cities:
            emp_list = emp_list.filter(city__in=selected_cities).values('city', 'job_name', 'company').distinct()
        if selected_jobs:
            emp_list = emp_list.filter(job_name__in=selected_jobs).values('city', 'job_name', 'company').distinct()

        paginator = Paginator(emp_list, 10)
        page = request.GET.get('page', '1')
        page_obj = paginator.get_page(page)
    else:
        # 초기 페이지 로드
        emp_list = EmpInfo.objects.all().values('city', 'job_name', 'company').distinct()
        paginator = Paginator(emp_list, 10)
        page = request.GET.get('page', '1')
        page_obj = paginator.get_page(page)

    context = {'emp_list': page_obj, 'city_list': city_list, 'job_list': job_list}
    return render(request, 'prediction/emp.html', context)

def search(request):
    city_list = EmpInfo.objects.values_list('city', flat=True).distinct()
    job_list = EmpInfo.objects.values_list('job_name', flat=True).distinct()

    if request.user.is_authenticated:
        if request.method == 'GET':
            selected_cities = request.GET.getlist("city")
            selected_jobs = request.GET.getlist("job_name")

            emp_list = EmpInfo.objects.all()

            if selected_cities:
                emp_list = emp_list.filter(city__in=selected_cities).values('city', 'job_name', 'company').distinct()
            if selected_jobs:
                emp_list = emp_list.filter(job_name__in=selected_jobs).values('city', 'job_name', 'company').distinct()

            return render(request, 'prediction/emp.html', {'city_list': city_list, 'job_list': job_list, 'emp_list': emp_list})
    else:
        return render(request, 'common/login.html')