import torch
import os
import dgl
from Dataloader import dataload
from torch.utils.data import SequentialSampler
from dgl.dataloading import GraphDataLoader

weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']

saved_model_path = os.path.abspath('../sku3343/dataset/model/ether frozen')
model = torch.load(saved_model_path)

model.eval()  # 모델을 평가 모드로 설정

# 데이터셋 불러오기
dataset_path = os.path.abspath('../sku3343/dataset/dgl_graph')
dataset = dataload('test', dataset_path)

dataset_len = len(dataset)
sampler = SequentialSampler(torch.arange(dataset_len))
dataloader = GraphDataLoader(dataset, sampler=sampler, batch_size=1, drop_last=False)


for batched_graph, labels in dataloader:
    # 예측 수행
    pred = model(batched_graph)

    print("\nPredictions:", pred)
    print("Actual Labels:", labels)
    print()
    
    
    
    #예측 수치
    # print("모델의 예측 수치:", pred)
    
    # #예측 결과 확인을 위한 출력
    print("예측 값:", torch.argmax(pred).item())
    # print("실제 값:", labels[0].item())
    
    
