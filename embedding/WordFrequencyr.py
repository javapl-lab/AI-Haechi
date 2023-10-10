import os
import re
from Graph_generator_for_GNN.parsing.Generator import generate


abs_code_path = os.path.abspath('../embedding/embedding_code')
abs_result_path = os.path.abspath('../result/embedding')
tmp = ['block number dependency']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
vocabulary = {}
preprocessed_sentences = []

for weakness in tmp:
    folder_path = abs_code_path + '\\' + weakness
    solidity_list = os.listdir(folder_path)
    count = 0
    result = []
    for file_name in solidity_list:
        file_path = folder_path + '\\' + file_name
        try:
            viz_code = generate(file_path, file_name)

            for word in viz_code:
                word = word.lower()
                result.append(word)
                if word not in vocabulary:
                    vocabulary[word] = 0
                vocabulary[word] += 1
            preprocessed_sentences.append(result)
            count += 1
            print('now...', count)

        except Exception as e:
            print(file_name + ": " + str(e))
            continue
#
vocabulary_sorted = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)

integer_encoding = open(abs_result_path + '/WordFrequencyr.txt', 'w+')
integer_encoding.write(str(vocabulary_sorted))
integer_encoding.close()

print('done')
