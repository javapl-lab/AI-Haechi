import os
os.environ["DGLBACKEND"] = "pytorch"
import sys
sys.path.insert(0, '/workspace/sku3343/heesung')

import torch
import torch.nn.functional as F
from dgl.dataloading import GraphDataLoader
from torch.utils.data import SubsetRandomSampler
from gnn_class.HeteroClassifier import HeteroClassifier
from learning.Dataloader import dataload


# cuda 사용 여부 확인
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

# 데이터셋 불러오기
weakness_list = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                    'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call', 'test']
weakness = weakness_list[4]
dataset_path = os.path.abspath('../sku3343/dataset/dgl_graph')
dataset = dataload(weakness, dataset_path)

# 학습 데이터 길이 80%, 나머지 20%를 검증 데이터로
dataset_len = len(dataset)
train_len = int(len(dataset) * 0.8)

print("dataset_len: ", dataset_len)
print("train_len: ", train_len)
print("validation_len: ", dataset_len - train_len)

train_sampler = SubsetRandomSampler(torch.arange(train_len))
validation_sampler = SubsetRandomSampler(torch.arange(train_len, dataset_len))
     
train_dataloader = GraphDataLoader(
    dataset, sampler = train_sampler, batch_size = 1, drop_last = False)
validation_dataloader = GraphDataLoader(
    dataset, sampler = validation_sampler, batch_size = 1, drop_last = False)
        
etypes = ['normal', 'false', 'true']

model = HeteroClassifier(128, 16, 2, etypes)
model.to('cuda')

opt = torch.optim.Adam(model.parameters())
epoch = 300
for i in range(1, epoch + 1):
    total_loss = 0
    cnt = 0
    for batched_graph, label in train_dataloader:
        logits = model(batched_graph)
        loss = F.cross_entropy(logits, label)
        opt.zero_grad()
        loss.backward()
        opt.step()
        
        # if cnt % 30 == 0:
            # print(logits)
        total_loss += loss.item()
        
        cnt += 1
        
    avg_loss = total_loss / len(train_dataloader)
    print("Epoch [{}/{}], Loss: {:.4f}".format(i, epoch, avg_loss))

num_correct = 0
num_tp = 0
num_fp = 0
num_fn = 0
num_tests = 0
cnt = 1

for batched_graph, labels in validation_dataloader:
    pred = model(batched_graph)
    
    # 예측 결과 확인을 위한 출력
    print(cnt, '---------------------')
    cnt += 1
    print("tensor:", pred)
    # print("Actual Labels:", labels)
    
    print("예측 값:", torch.argmax(pred).item())
    print("실제 값:", labels[0].item())
    
    # 정확도 측정 / accurancy
    num_correct += (pred.argmax(1) == labels).sum().item()
    
    # 정밀도 측정 / precision
    num_tp += ((pred.argmax(1) == 1) & (labels == 1)).sum().item()
    num_fp += ((pred.argmax(1) == 1) & (labels == 0)).sum().item()
    
    # 재현율 측정 / recall
    num_fn += ((pred.argmax(1) == 0) & (labels == 1)).sum().item()

    num_tests += len(labels)


accurancy = num_correct / num_tests
precision = num_tp / (num_tp + num_fp) if (num_tp + num_fp) > 0 else 0.0
recall = num_tp / (num_tp + num_fn) if (num_tp + num_fn) > 0 else 0.0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

print(f'accuracy:', accurancy)
print(f'precision:', precision)
print(f'recall:', recall)
print(f'F1 Score:', f1_score)

torch.save(model, os.path.abspath('../sku3343/dataset/model/{0}'.format(weakness)))
