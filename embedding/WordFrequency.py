import os
import re

import sys
sys.path.insert(0, '/workspace/sku3343/heesung')

from parsing.Generator import generate


def word_frequency(file_path, result_path):
    weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                    'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
    vocabulary = {}
    preprocessed_sentences = []

    success_count = 0
    fail_count = 0
    success_file = []
    fail_file = []

    for weakness in weakness_name:
        weakness_count = 0
        folder_path = file_path + '/solidity/' + weakness
        print("폴더경로: ", folder_path)
        solidity_list = os.listdir(folder_path)
        result = []
        for file_name in solidity_list:
            try:
                viz_code = generate(folder_path + '/' + file_name, file_name, result_path)
                
                viz_code = (viz_code.strip().split('\n'))
                
                # 정규식을 사용해 viz_code로 부터 데이터 추출
                for line in viz_code:
                    if '->' not in line and 'rank' not in line:
                        if 'label' in line:
                            line = re.sub(r'\"|\]|;', '', line)
                            line = line.split(' ')[-1]
                        else:
                            line = re.sub(r'\];|, shape = diamond\];|"|}|,', '', line)
                    
                        for token in line.split(' '):
                            result.append(token)
                            if token not in vocabulary:
                                vocabulary[token] = 0
                            vocabulary[token] += 1
                        preprocessed_sentences.append(result)
                
                success_count += 1
                weakness_count += 1
                success_file.append(file_name)
                print('now...', file_name)
                
                if weakness_count == 100:
                    weakness_count = 0
                    break

            except Exception as e:
                fail_count += 1
                fail_file.append(file_name)
                print(file_name + ": " + str(e))

                continue

            print('success:', success_count)
            print('fail:', fail_count)
            
    try:
        vocabulary.pop('')
    except KeyError:
        pass    
        
    vocabulary_sorted = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)

    integer_encoding = open(result_path + '/WordFrequency.txt', 'w+')
    integer_encoding.write(str(vocabulary_sorted))
    integer_encoding.close()

    print('done')