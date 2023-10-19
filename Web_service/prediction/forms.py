from django import forms
from prediction.models import *

class EmpPredictionForm(forms.ModelForm):
    class Meta:
        model = PredictionResult
        fields = ['date', 'city', 'industry', 'result', 'user_id']