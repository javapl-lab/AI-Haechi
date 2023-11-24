import os
import pickle


total = 0
fail = 0

abs_result_path = os.path.abspath('../Graph_generator_for_GNN/result/dgl_graph')
tmp = ['block number dependency']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']


for weakness in weakness_name:
    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness, '--------------------------------------')

    dgl_list = os.listdir(save_folder_path)

    for file_name in dgl_list:
        save_file_path = save_folder_path + '\\' + file_name.split('.')[0]

        with open(save_file_path,'rb') as f:
            data = pickle.load(f)

        print(file_name, '-------------------------')
        print(data)
        total += 1
        if data is None:
            fail += 1


print(fail, '/', total)


