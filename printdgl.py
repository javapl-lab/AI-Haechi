import os
import pickle


total = 0
fail = 0

abs_result_path = os.path.abspath('../Graph_generator_for_GNN/embedding/embedding_code')
tmp = ['block number dependency']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']





for weakness in weakness_name:
    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness, '--------------------------------------')

    dgl_list = os.listdir(save_folder_path)
    count =0
    for file_name in dgl_list:
        count += 1
    print(count)


