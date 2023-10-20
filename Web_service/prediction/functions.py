from .apps import PredictionConfig
import pandas as pd
from pickle import load
import torch
from torch import nn
import numpy as np
from torch.autograd import Variable
import os
from django.conf import settings

def prediction(data):
    # data에서 넘어오는 컬럼: date, city, industry
    temp = PredictionConfig.pred_temp.copy()
    temp['date'] = data['date'].values[0]
    city = data['city'].values[0]
    industry = data['industry'].values[0]
    if city in temp.columns:
        temp[f'{city}'] = 1.0
    if industry in temp.columns:
        temp[f'{industry}'] = 1.0
    # 지역, 산업, 월에 따른 데이터 추출
    pred_data = PredictionConfig.pred_value.loc[(PredictionConfig.pred_value['date'] == data['date'].values[0])&
                                                (PredictionConfig.pred_value['city'] == data['city'].values[0])&
                                                (PredictionConfig.pred_value['industry'] == data['industry'].values[0])]
    # 템플릿에 데이터 삽입
    temp[['employment', 'no_company', 'unemployment',
          'population', 'GDP', 'i_rate', 'CLI', 'CFI']] = pred_data[['employment', 'no_company', 'unemployment', 'population',
                                                                     'GDP', 'i_rate', 'CLI', 'CFI']].values
    # set index
    temp['date'] = pd.to_datetime(temp['date'], format='%Y%m')
    temp.set_index('date', inplace=True)
    
    # log 변환 및 Scale 작업
    temp[['employment', 'no_company', 'unemployment', 'population', 'GDP', 'i_rate', 'CLI', 'CFI']] = np.log1p(temp[['employment', 'no_company', 'unemployment', 'population', 'GDP', 'i_rate', 'CLI', 'CFI']])
    temp[['employment', 'no_company', 'unemployment', 'population', 'GDP', 'i_rate', 'CLI', 'CFI']] = PredictionConfig.x_label_scaler.transform(temp[['employment', 'no_company', 'unemployment', 'population', 'GDP', 'i_rate', 'CLI', 'CFI']])
    
    # na값 채우기
    temp.fillna(0.0, inplace=True)
    
    # 텐서 형태 변환
    pred_x_tensors = Variable(torch.Tensor(temp.values))
    pred_x_tensors_f = torch.reshape(pred_x_tensors, (pred_x_tensors.shape[0], 1, pred_x_tensors.shape[1]))
    
    class LSTM(nn.Module):
        def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
            super(LSTM, self).__init__()
            self.num_classes = num_classes  # 클래스 개수
            self.num_layers = num_layers    # LSTM 계층의 개수
            self.input_size = input_size    # 입력 크기
            self.hidden_size = hidden_size  # 은닉층의 뉴런 개수
            self.seq_length = seq_length    # 시퀀스 길이
            
            self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)    # LSTM 계층
            self.bn_2 = nn.BatchNorm1d(4)
            self.fc_1 = nn.Linear(hidden_size, 128) # 완전 연결층
            self.bn_1 = nn.BatchNorm1d(128)
            self.fc = nn.Linear(128, num_classes)   # 출력층
            self.relu = nn.ReLU()
        
        def forward(self, x):
            h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))   # 은닉 상태를 0으로 초기화
            c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size))   # 셀 상테를 0으로 초기화
            output, (hn, cn) = self.lstm(x, (h_0, c_0)) # LSTM 계층에 은닉 상태와 셀 상태 적용
            hn = hn.view(-1, self.hidden_size)  # 완전연결층 적용을 위해 데이터의 형태 조정
            out = self.bn_2(hn)
            out = self.relu(out)
            out = self.fc_1(out)
            out = self.bn_1(out)
            out = self.relu(out)
            out = self.fc(out)
            return out
    
    static_url = os.path.join(settings.BASE_DIR, 'static')
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = LSTM(1, 28, 4, 1, 1)
    model.load_state_dict(torch.load(os.path.join(static_url, 'LSTM_모델_dict.pt'), map_location=device))
    
    # 예측 및 결과 변환
    with torch.no_grad():
        model.eval()
        single_prediction = model(pred_x_tensors_f)
    
    result = single_prediction.data.numpy()
    result = PredictionConfig.y_label_scaler.inverse_transform(result)
    result = np.expm1(result)
    result = int(result)
    return result