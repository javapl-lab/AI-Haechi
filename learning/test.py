import dgl
import torch
from dgl.nn.pytorch import GraphConv
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dgl.data import DGLDataset
import pandas as pd
import os
import pickle


abs_result_path = os.path.abspath('D:/dgl_graph')
tmp = ['dangerous delegatecall']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']

# 라벨 데이터 가져오기
csv_file_path = 'output.csv'
csv_data = pd.read_csv(csv_file_path)

# 그래프 데이터 가져오기
graph_list = []
for weakness in tmp:
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
            else:
                # 리스트에 그래프 추가
                graph_list.append(data)

                # 리스트에 보안약점 여부 추가
                ground_truth = folder_data[folder_data['file'] == int(file_name)]['ground truth'].tolist()[0]
                ground_truth_list.append(ground_truth)
                print(file_name, ', ', ground_truth)
