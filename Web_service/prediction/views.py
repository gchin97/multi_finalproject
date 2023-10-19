from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import EmpPredictionForm
from .models import *
from django.core.paginator import Paginator
from .functions import prediction
import pandas as pd

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
            predict = form.save(commit=False) # 입력 데이터 들고오기
            predict_data = pd.DataFrame({'date':predict.date, 'industry':predict.industry, 'city':predict.city}, index=[0])
            result = prediction(predict_data)
            predict.result = result
            form.save()
            context = {'result':result, 'city':predict.city, 'industry':predict.industry}
            return render(request, 'prediction/predict.html', context=context)
    else:
        form = EmpPredictionForm()
    context = {'form':form}
    return render(request, 'prediction/predict.html', context)

def emp(request):
    city_list = EmpInfo.objects.values_list('city', flat=True).distinct()
    job_list = EmpInfo.objects.values_list('job_name', flat=True).distinct()

    # 초기 페이지 로드
    emp_list = EmpInfo.objects.all().values('city', 'job_name', 'company', 'link', 'ncs_code').distinct()
    education_list = Education.objects.all().values('train_title', 'start_date', 'end_date', 'train_center', 'quota', 'link').distinct()
    center_list = EducationCenter.objects.filter(train_center__in=education_list.values_list('train_center', flat=True)).values('address', 'center_tel').distinct()

# 고유한 'city', 'company', 'link', 'job_name' 정보를 포함하는 사전의 목록
    unique_emp_list = []

    for emp in emp_list:
        city = emp['city']
        job_name = emp['job_name']
        company = emp['company']
        link = emp['link']

        # 이미 목록에 있는 회사와 직업인지 확인하고 중복을 방지합니다.
        if not any(entry['company'] == company and entry['job_name'] == job_name  for entry in unique_emp_list):
            unique_emp_list.append({'city': city, 'job_name': job_name, 'company': company, 'link': link})


    paginator = Paginator(unique_emp_list, 5)
    page = request.GET.get('page', '1')
    page_obj = paginator.get_page(page)

    context = {'emp_list': page_obj, 'city_list': city_list, 'job_list': job_list, 'education_list' : education_list, 'center_list': center_list}
    return render(request, 'prediction/emp.html', context)
    
def search(request):
    city_list = EmpInfo.objects.values_list('city', flat=True).distinct()
    job_list = EmpInfo.objects.values_list('job_name', flat=True).distinct()

    error_message = None

    if request.user.is_authenticated:
        if request.method == 'GET':
            selected_cities = request.GET.getlist("city")
            selected_jobs = request.GET.getlist("job_name")

            # selected_jobs에 있는 각 직업의 ncs_code를 가져옴
            ncs_codes = EmpInfo.objects.filter(job_name__in=selected_jobs).values_list('ncs_code', flat=True).distinct()
            emp_list = EmpInfo.objects.all()
            education_list = Education.objects.all()
                
            if selected_cities:
                emp_list = emp_list.filter(city__in=selected_cities).values('city', 'job_name', 'company', 'link', 'ncs_code').distinct()

            if selected_jobs:
                emp_list = emp_list.filter(job_name__in=selected_jobs).values('city', 'job_name', 'company', 'link', 'ncs_code').distinct()
                education_list = education_list.filter(ncs_code__in=ncs_codes).distinct()

            if not selected_cities and not selected_jobs:
                    error_message = "적어도 하나의 지역 또는 직업을 선택해주세요."
                    emp_list = []  
                    education_list = []              

            # 고유한 'city', 'company', 'link', 'job_name' 정보를 포함하는 사전의 목록
            unique_emp_list = []

            for emp in emp_list:
                city = emp['city']
                job_name = emp['job_name']
                company = emp['company']
                link = emp['link']

                # 이미 목록에 있는 회사와 직업인지 확인하고 중복을 방지합니다.
                if not any(entry['company'] == company and entry['job_name'] == job_name  for entry in unique_emp_list):
                    unique_emp_list.append({'city': city, 'job_name': job_name, 'company': company, 'link': link})

            paginator = Paginator(unique_emp_list, 5)
            page = request.GET.get('page', '1')
            page_obj = paginator.get_page(page)

            return render(request, 'prediction/emp.html', {'city_list': city_list, 'job_list': job_list, 'education_list' : education_list, 'emp_list': page_obj , 'error_message':error_message})
    else:
        return render(request, 'common/login.html')
    