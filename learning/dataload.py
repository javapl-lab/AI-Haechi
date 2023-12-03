import os
import pickle
import torch
import dgl.data
from dgl.data import DGLDataset
import dgl.nn.pytorch as dglnn
import torch.nn as nn
import pandas as pd
import torch.nn.functional as F

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
folder_path_delegate = 'dgl_graph/dangerous delegatecall'
# folder_path_integer = 'dgl_graph/integer overflow'
folder_path_timestamp = 'dgl_graph/timestamp dependency'
folder_path_reentrancy = 'dgl_graph/reentrancy'

# List to hold the loaded pickle data
loaded_pickles_delegate = []
# loaded_pickles_integer = []
loaded_pickles_timestamp = []
loaded_pickles_reentrancy = []

# Check if the folder exists
# if os.path.exists(folder_path_delegate):
#     # Iterate through each file in the folder
#     for filename in os.listdir(folder_path_delegate):
#         # Check if the file is a pickle file
#             # Construct the full file path
#             file_path = os.path.join(folder_path_delegate, filename)
#             # Open and load the pickle file
#             with open(file_path, 'rb') as file:
#                 data = pickle.load(file)
#                 if data is not None:
#                     # Append the loaded data to the list
#                     loaded_pickles_delegate.append(data)
#                 else:
#                     print(f"File '{filename}' is None.")
# else:
#     print(f"Folder '{folder_path_delegate}' does not exist.")

# #print(loaded_pickles_delegate[:5])

# # Check if integer Overflow
# # if os.path.exists(folder_path_integer):
# #     # Iterate through each file in the folder
# #     for filename in os.listdir(folder_path_integer):
# #         # Check if the file is a pickle file
# #             # Construct the full file path
# #             file_path = os.path.join(folder_path_integer, filename)
# #             # Open and load the pickle file
# #             with open(file_path, 'rb') as file:
# #                 data = pickle.load(file)
# #                 # Append the loaded data to the list
# #                 loaded_pickles_integer.append(data)
# # else:
# #     print(f"Folder '{folder_path_integer}' does not exist.")

# # print(loaded_pickles_integer[:5])

# Check if timestamp
# if os.path.exists(folder_path_timestamp):
#     # Iterate through each file in the folder
#     for filename in os.listdir(folder_path_timestamp):
#         # Check if the file is a pickle file
#             # Construct the full file path
#             file_path = os.path.join(folder_path_timestamp, filename)
#             # Open and load the pickle file
#             with open(file_path, 'rb') as file:
#                 data = pickle.load(file)
#                 # Append the loaded data to the list
#                 if data is not None:
#                     # Append the loaded data to the list
#                     loaded_pickles_delegate.append(data)
#                 else:
#                     print(f"File '{filename}' is None.")
# else:
#     print(f"Folder '{folder_path_timestamp}' does not exist.")

#print(loaded_pickles_timestamp[:5])

# Check if reentrancy
# if os.path.exists(folder_path_reentrancy):
#     # Iterate through each file in the folder
#     for filename in os.listdir(folder_path_reentrancy):
#         # Check if the file is a pickle file
#             # Construct the full file path
#             file_path = os.path.join(folder_path_reentrancy, filename)
#             # Open and load the pickle file
#             with open(file_path, 'rb') as file:
#                 data = pickle.load(file)
#                 if data is not None:
#                     # Append the loaded data to the list
#                     loaded_pickles_delegate.append(data)
#                 else:
#                     print(f"File '{filename}' is None.")
# else:
#     print(f"Folder '{folder_path_reentrancy}' does not exist.")

# #print(loaded_pickles_reentrancy[:5])

file_path1 = 'dgl_graph/dangerous delegatecall/510'
file_path2 = 'dgl_graph/dangerous delegatecall/1517'

# pickle 파일로부터 그래프 객체 로드
with open(file_path1, 'rb') as f:
    graph_510 = pickle.load(f)

with open(file_path2, 'rb') as f:
    graph_1517 = pickle.load(f)

total_data =[graph_510, graph_510]

print(len(total_data))

df_labels = pd.read_csv('combined_ground_truth.csv')
labels = [1,1]
print(len(labels))

dataset = MyCustomDataset(total_data, labels)

from dgl.dataloading import GraphDataLoader
dataloader = GraphDataLoader(
    dataset,
    batch_size=1,
    drop_last=False,
    shuffle=True)

for i, (batched_graph, labels) in enumerate(dataloader):
    print(f"배치 {i}:")
    print(f"  노드 수: {batched_graph.number_of_nodes()}")
    print(f"  엣지 수: {batched_graph.number_of_edges()}")
    print(f"  노드 타입: {batched_graph.ntypes}")
    print(f"  엣지 타입: {batched_graph.etypes}")

etypes = ['normal', 'false', 'true']
model = HeteroClassifier(342, 20, 2, etypes)

opt = torch.optim.Adam(model.parameters())
for epoch in range(20):
    for batched_graph, labels in dataloader:
        logits = model(batched_graph)
        loss = F.cross_entropy(logits, labels)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print('ok')
