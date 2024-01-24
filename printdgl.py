import os
import pickle


total = 0
fail = 0

# abs_result_path = os.path.abspath('../Graph_generator_for_GNN/embedding/embedding_code')
# tmp = ['block number dependency']
# weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
#                  'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
#
#
#
#
# # 보안약점 항목별 데이터 개수 출력
# for weakness in weakness_name:
#     save_folder_path = abs_result_path + '\\' + weakness
#     print(weakness, '--------------------------------------')
#
#     dgl_list = os.listdir(save_folder_path)
#     count =0
#     for file_name in dgl_list:
#         count += 1
#     print(count)


abs_result_path = os.path.abspath('D:/dgl_graph')
tmp = ['block number dependency']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']


for weakness in weakness_name:
    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness, '--------------------')

    dgl_list = os.listdir(save_folder_path)

    for file in dgl_list:
        save_file_path = save_folder_path + '\\' + file
        print(file + '.sol --------------------------------------')

        with open(save_file_path,'rb') as f:
            data = pickle.load(f)

            #그래프의 노드 수를 반환
            num_nodes = data.num_nodes()
            print(f"Number of nodes: {num_nodes}")

            # 그래프의 엣지 수를 반환
            num_edges = data.num_edges()
            print(f"Number of edges: {num_edges}")

            # 그래프 전체 반환
            print(data)

            print('\n\n\n')
