from django.apps import AppConfig
from django.conf import settings
from pickle import load
import torch
from torch import nn
import pandas as pd
from torch.autograd import Variable
import os

static_url = os.path.join(settings.BASE_DIR, 'static')

class PredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prediction'
    pred_temp = pd.read_csv(os.path.join(static_url, 'prediction_df_template.csv'), encoding='cp949')
    x_label_scaler = load(open(os.path.join(static_url, 'X_label_scaler.pkl'), 'rb'))
    y_label_scaler = load(open(os.path.join(static_url, 'Y_label_scaler.pkl'), 'rb'))
    pred_value = pd.read_csv(os.path.join(static_url, 'pred_data.csv'), encoding='utf-8')
    