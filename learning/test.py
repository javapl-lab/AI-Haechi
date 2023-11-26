import dgl
import torch
from dgl.nn.pytorch import GraphConv
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dgl.data import DGLDataset

import os
import pickle


abs_result_path = os.path.abspath('../result/dgl_graph')
tmp = ['block number dependency']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']

graph_list = []
for weakness in tmp:
    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness, '--------------------------------------')

    dgl_list = os.listdir(save_folder_path)

    for file_name in dgl_list:
        save_file_path = save_folder_path + '\\' + file_name.split('.')[0]

        with open(save_file_path,'rb') as f:
            data = pickle.load(f)
            if data is None:
                pass
            else:
                graph_list.append(data)





class GCN(nn.Module):
    def __init__(self, in_feats, h_feats, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, h_feats)
        self.conv2 = GraphConv(h_feats, num_classes)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        g.ndata['h'] = h
        return dgl.mean_nodes(g, 'h')
class MyCustomDataset(DGLDataset):
    def __init__(self, graph_list):
        self.graph_list = graph_list
        super().__init__(name='custom_dataset')

    def process(self):
        # 이 메소드에서는 self.graph_list에 있는 그래프들을 처리합니다.
        # 예시에서는 추가적인 처리를 하지 않았습니다.
        self.graphs = self.graph_list

    def __getitem__(self, i):
        # i번째 그래프를 반환합니다.
        return self.graphs[i]

    def __len__(self):
        # 데이터셋에 있는 그래프의 총 개수를 반환합니다.
        return len(self.graphs)

# MyCustomDataset 인스턴스 생성
dataset = MyCustomDataset(graph_list)



print('...................................................................')

batch_size = 64
train_dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

model = GCN(348, 16, 2)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(20):
    for batched_graph, labels in train_dataloader:
        pred = model(batched_graph, batched_graph.ndata['expression'].float())
        loss = F.cross_entropy(pred, labels)
        loss.backward()
        optimizer.step()