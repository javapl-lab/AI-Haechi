import os
import pickle
import torch
import dgl.data
from dgl.data import DGLDataset
import dgl.nn.pytorch as dglnn
import torch.nn as nn
import pandas as pd
import torch.nn.functional as F
from torch.utils.data import SubsetRandomSampler


class RGCN(nn.Module):
    def __init__(self, in_feats, hid_feats, out_feats, rel_names):
        super().__init__()

        self.conv1 = dglnn.HeteroGraphConv({
            rel: dglnn.GraphConv(in_feats, hid_feats)
            for rel in rel_names}, aggregate='sum')
        self.conv2 = dglnn.HeteroGraphConv({
            rel: dglnn.GraphConv(hid_feats, out_feats)
            for rel in rel_names}, aggregate='sum')

    def forward(self, graph, inputs):
        # inputs is features of nodes
        h = self.conv1(graph, inputs)
        h = {k: F.relu(v) for k, v in h.items()}
        h = self.conv2(graph, h)
        return h


class HeteroClassifier(nn.Module):
    def __init__(self, in_dim, hidden_dim, n_classes, rel_names):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.rgcn = RGCN(in_dim, hidden_dim, hidden_dim, rel_names)
        self.classify = nn.Linear(hidden_dim, n_classes)

    def forward(self, g):
        h = g.ndata['feat']
        h = self.rgcn(g, h)

        with g.local_scope():
            for ntype in h:
                g.nodes[ntype].data['h'] = h[ntype]

            hg = torch.zeros((1, self.hidden_dim))  # hidden_dim 사용
            for ntype in g.ntypes:
                if 'h' in g.nodes[ntype].data:
                    hg = hg + dgl.mean_nodes(g, 'h', ntype=ntype)

            return self.classify(hg)


class MyCustomDataset(DGLDataset):
    def __init__(self, graph_list, labels):
        self.graph_list = graph_list
        self.labels = labels
        super().__init__(name='custom_dataset')

    def process(self):
        # 이 메소드에서는 self.graph_list에 있는 그래프들을 처리합니다.
        # 예시에서는 추가적인 처리를 하지 않았습니다.
        self.graphs = self.graph_list
        self.label_tensor = torch.tensor(self.labels)

        for i, graph in enumerate(self.graph_list):
            # 메타그래프에서 정의된 노드 타입을 가져옵니다.
            defined_node_types = set(graph.ntypes)

            # 그래프의 각 노드 타입을 검사합니다.
            for ntype in graph.ndata['ntype']:
                if ntype not in defined_node_types:
                    print(f"그래프 {i}에서 정의되지 않은 노드 타입 '{ntype}'을(를) 발견했습니다.")
                else:
                    print(f"그래프 {i}는 정상적인 노드 타입 '{ntype}'을(를) 가지고 있습니다.")

    def __getitem__(self, i):
        # i번째 그래프를 반환합니다.
        return self.graphs[i], self.label_tensor[i]

    def __len__(self):
        # 데이터셋에 있는 그래프의 총 개수를 반환합니다.
        return len(self.graphs)


# Define the path to the 'block number dependency' folder inside 'dgl_graph'
abs_result_path = os.path.abspath('D:/dgl_graph')
tmp = ['ether strict equality']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
counter = 0


# 그래프 데이터 가져오기
graph_list = []
for weakness in tmp:

    # 라벨 데이터 가져오기
    csv_file_path = f'output_{weakness}.csv'
    csv_data = pd.read_csv(csv_file_path)

    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness, '--------------------------------------')

    folder_data = csv_data[csv_data['folder'] == weakness]
    ground_truth_list = []


    dgl_list = os.listdir(save_folder_path)
    for file_name in dgl_list:
        save_file_path = save_folder_path + '\\' + file_name

        with open(save_file_path,'rb') as f:
            data = pickle.load(f)
            if data is None:
                pass
            elif int(file_name) not in folder_data['file'].values: # dgl 그래프는 있는데 해당 그래프에 대한 라벨이 존재하지 않는 경우가 있다.
                print(f"File {file_name} not found in folder_data. Skipping.")
                #pass
            else:
                # 리스트에 그래프 추가
                graph_list.append(data)

                # 리스트에 보안약점 여부 추가
                counter+=1
                print('---------------', counter)
                print(file_name)
                ground_truth = folder_data[folder_data['file'] == int(file_name)]['ground truth'].tolist()[0]
                ground_truth_list.append(ground_truth)
                print(ground_truth)




total_data = graph_list
labels = ground_truth_list

print(len(total_data))

# df_labels = pd.read_csv('combined_ground_truth.csv')
# labels = df_labels['label'].tolist()
print(len(labels))

dataset = MyCustomDataset(total_data, labels)

from dgl.dataloading import GraphDataLoader

num_examples = len(dataset)
num_train = int(num_examples * 0.8)

train_sampler = SubsetRandomSampler(torch.arange(num_train))
test_sampler = SubsetRandomSampler(torch.arange(num_train, num_examples))

train_dataloader = GraphDataLoader(
    dataset, sampler=train_sampler, batch_size=1, drop_last=False)
test_dataloader = GraphDataLoader(
    dataset, sampler=test_sampler, batch_size=1, drop_last=False)

etypes = ['normal', 'false', 'true']
model = HeteroClassifier(342, 20, 2, etypes)

opt = torch.optim.Adam(model.parameters())
for epoch in range(20):
    for batched_graph, labels in train_dataloader:
        logits = model(batched_graph)
        loss = F.cross_entropy(logits, labels)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print('ok')


num_correct = 0
num_tests = 0

for batched_graph, labels in test_dataloader:
    pred = model(batched_graph)
    num_correct += (pred.argmax(1) == labels).sum().item()
    num_tests += len(labels)

print(f'{tmp[0]} accuracy:', num_correct / num_tests)