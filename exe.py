from Graph_generator_for_GNN.parsing.Generator import generate
import os
import pickle

# file_name = '0.sol'
#
# file_path = os.path.abspath('../Graph_generator_for_GNN/embedding/embedding_code/block number dependency/' + file_name)
# dgl = generate(file_path, file_name)
#
# print(dgl)



abs_code_path = os.path.abspath('../Graph_generator_for_GNN/embedding/embedding_code')
abs_result_path = os.path.abspath('D:/dgl_graph')
tmp = ['dangerous delegatecall']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']

success_count = 0
fail_count = 0
success_file = []
fail_file = []
max = 0

for weakness in tmp:
    folder_path = abs_code_path + '\\' + weakness
    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness)

    solidity_list = os.listdir(folder_path)

    for file_name in solidity_list:
        file_path = folder_path + '\\' + file_name
        save_file_path = save_folder_path + '\\' + file_name.split('.')[0]
        try:
            print(file_name)
            dgl_graph = generate(file_path, file_name)


            with open(save_file_path, 'wb') as f:
                pickle.dump(dgl_graph, f)

            success_count += 1
            success_file.append(file_name)
            print('now...', file_name)
            # if success_count == 100:
            #     success_count = 0
            #     break

        except Exception as e:
            fail_count += 1
            fail_file.append(file_name)
            print(file_name + ": " + str(e))

            continue

        print('success:', success_count)
        # print('success:', success_file)
        print('fail:', fail_count)
        # print('fail:', fail_file)

print('done')