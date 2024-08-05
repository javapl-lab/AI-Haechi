import pandas as pd
import os
import sys
sys.path.insert(0, '/workspace/sku3343/heesung')
from learning.gnn_class.MyCustomDataset import MyCustomDataset

def dataload(weakness, dataset_path):
    dgl_graph_list = os.listdir(dataset_path + f'/{weakness}')
    label_csv = pd.read_csv(dataset_path + f'/{weakness}.csv')
    label_dict = {file: label for file, label in zip(label_csv['file'].values, label_csv['label']) if str(file) in dgl_graph_list}
    dgl_graph_list = [item for item in dgl_graph_list if int(item) in label_dict]
    
    dataset = MyCustomDataset(dataset_path + f'/{weakness}', dgl_graph_list, label_dict)
    
    positive_class_ratio = sum(value == 1 for value in label_dict.values()) / len(label_dict)
    print("positive_class_ratio:", positive_class_ratio)
    
    return dataset
    
# dataset_path = os.path.abspath('../sku3343/dataset/dgl_graph/')
# dataset = dataload(0, dataset_path)
# print(dataset[0])