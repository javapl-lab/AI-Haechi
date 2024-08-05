import torch
import dgl
from dgl.data import DGLDataset

class MyCustomDataset(DGLDataset):
    def __init__(self, dataset_path, dgl_graph_list, label_dict):
        self.dataset_path = dataset_path
        self.dgl_graph_list = dgl_graph_list
        self.label_dict = label_dict
        super().__init__(name='custom_dataset')

    def __getitem__(self, i):
        dataset_path = self.dataset_path
        dgl_graph_list = self.dgl_graph_list
        label_dict = self.label_dict
        
        g, _ = dgl.load_graphs(dataset_path + '/' + dgl_graph_list[i])
        g = g[0].to('cuda')
        
        label = torch.tensor(label_dict[int(dgl_graph_list[i])])
        label = label.to('cuda')
        
        # print(dgl_graph_list[i]) 학습에 사용된 그래프 번호 출력용
        
        return g, label

    def __len__(self):
        return len(self.dgl_graph_list)