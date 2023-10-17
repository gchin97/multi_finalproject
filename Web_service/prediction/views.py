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
    if request.method == 'POST':
        return render(request, 'prediction/emp.html')
    else:
        page = request.GET.get('page', '1')
        emp_list = EmpInfo.objects.distinct()
        paginator = Paginator(emp_list, 10)
        page_obj = paginator.get_page(page)
        context = {'emp_list':page_obj} # 오류 발생으로 emp_info foreign key 삭제(직업명)
        return render(request, 'prediction/emp.html', context=context)

def search(self, request):
        city           = request.GET.getlist('city', None)
        job_name            = request.GET.getlist('job_name', None)

        if color:
            products = products.filter(productoption__city__in=city).distinct()

        if size:
            products = products.filter(productoption__job_name=job_name).distinct()