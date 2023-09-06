from solidity_parser import parser
import os
import re


weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
vocabulary = {}
preprocessed_sentences = []

for weakness in weakness_name:
    folder_path = r'C:\Users\wlfkr\Desktop\seminar\dataset' + '\\' + weakness
    solidity_list = os.listdir(folder_path)

    count = 0
    result = []
    for i in solidity_list:
        file_path = folder_path + '\\' + i
        try:
            solidity_file = open(file_path, 'r')
            ast = parser.parse(solidity_file.read(), loc=False)
            ast_prepro = re.sub(r'[{}:\'"",\[\]]', '', str(ast))
            ast_prepro = ast_prepro.split(' ')

            for word in ast_prepro:
                word = word.lower()
                result.append(word)
                if word not in vocabulary:
                    vocabulary[word] = 0
                vocabulary[word] += 1
            preprocessed_sentences.append(result)
            solidity_file.close()
            count += 1
            print('now...', count)

        except(Exception, ):
            print(i + ": " + str(Exception))
            continue

vocabulary_sorted = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)

target_file_path = r'C:\Users\wlfkr\Desktop' + '\\' + 'integer_encoding'
integer_encoding = open(target_file_path + '.txt', 'w+')
integer_encoding.write(str(vocabulary_sorted))
integer_encoding.close()

print('done')
