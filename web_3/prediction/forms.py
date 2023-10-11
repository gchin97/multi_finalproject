from django import forms
from prediction.models import *

class EmpPredictionForm(forms.ModelForm):
    class Meta:
        model = EmpPrediction
        fields = ['city', 'industry', 'job_offer', 'job_search',
                  'no_company', 'unemployment', 'population', 'gdp',
                  'i_rate', 'cli', 'cfi']