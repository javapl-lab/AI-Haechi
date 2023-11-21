import os
from Graph_generator_for_GNN.parsing.Generator import generate
import pickle


abs_code_path = os.path.abspath('../embedding/embedding_code')
abs_result_path = os.path.abspath('../result/dgl_graph')
tmp = ['block number dependency']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
vocabulary = {}
preprocessed_sentences = []

success_count = 0
fail_count = 0
success_file = []
fail_file = []

for weakness in tmp:
    folder_path = abs_code_path + '\\' + weakness
    save_folder_path = abs_result_path + '\\' + weakness

    solidity_list = os.listdir(folder_path)

    for file_name in solidity_list:
        file_path = folder_path + '\\' + file_name
        save_file_path = save_folder_path + '\\' + file_name.split('.')[0]
        try:
            dgl_graph = generate(file_path, file_name)




            with open(save_file_path, 'wb') as f:
                pickle.dump(dgl_graph, f)


            success_count += 1
            success_file.append(file_name)
            print('now...', file_name)
            if success_count == 50:
                break

        except Exception as e:
            fail_count += 1
            fail_file.append(file_name)
            print(file_name + ": " + str(e))

            continue

        print('success:', success_count)
        print('success:', success_file)
        print('fail:', fail_count)
        print('fail:', fail_file)

# vocabulary_sorted = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)
#
# integer_encoding = open(abs_result_path + '/WordFrequency.txt', 'w+')
# integer_encoding.write(str(vocabulary_sorted))
# integer_encoding.close()

print('done')