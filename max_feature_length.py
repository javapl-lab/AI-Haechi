import os
import re
import pickle
from Graph_generator_for_GNN.parsing.AstToCFG import ast_to_cfg
from Graph_generator_for_GNN.parsing.SolidityToAST import solidity_to_ast

def extraction(viz_code):
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

    dgl_U, dgl_V = [], []
    node_dict = dict()
    edge_list = []
    feature_dict = dict()
    feature_list = []
    node_id = 0
    normalization = open(os.path.abspath('../Graph_generator_for_GNN/result/embedding/Normalization.txt'), 'r').read()
    normalization_dict = eval(normalization)

    viz_edges = re.findall(r'\d+ -> \d+', viz_code)
    for i in viz_edges:
        dgl_U.append(int(i.split()[0]))
        dgl_V.append(int(i.split()[2]))

    viz_code = (viz_code.strip().split('\n'))
    # 정규식을 사용해 viz_code로 부터 데이터 추출
    for line in viz_code:
        # node_dict를 먼저 생성
        if re.findall(r'\d+ \[label = ', line):
            node_id = line.split()[0]
            feature_list = []
            if ' -> ' not in line:
                node_dict[line.split()[0]] = re.sub(r"[^a-zA-Z]", "", line.split()[3])

        # feature_dict를 생성
        if '{' not in line and '[' not in line and '->' not in line:
            pattern = re.compile(r'"(.*?);')
            line = re.sub(pattern, '', line)

            if ']' in line:
                line = ' '.join(line.split()[:-1])
            if 'shape' in line:
                line = ' '.join(line.split()[:-3])
            line = line.split(' ')
            for token in line:
                if token != '':
                    if token in normalization_dict:
                        feature_list.append(normalization_dict[token])
                    else:
                        feature_list.append(1)
            feature_dict[node_id] = feature_list

    for line in viz_code:
        # nodedict를 사용해 edge_dict를 생성
        if '->' in line:
            if 'label' in line:
                edge_list.append((line.split()[0], re.sub(r"[^a-zA-Z]", "", line.split()[5]), line.split()[2]))
            else:
                edge_list.append((line.split()[0], 'normal', re.sub(';', '', line.split()[2])))

    # 맨 마지막 키인 '}'를 딕셔너리에서 제거
    last_key = list(feature_dict.keys())[-1]
    del feature_dict[last_key]

    # 가장 긴 특징의 길이
    max_feature_length = 0
    for key in feature_dict:
        if max_feature_length < len(feature_dict[key]):
            max_feature_length = len(feature_dict[key])

    return max_feature_length




abs_code_path = os.path.abspath('../Graph_generator_for_GNN/embedding/embedding_code')
abs_result_path = os.path.abspath('../Graph_generator_for_GNN/result/dgl_graph')
tmp = ['ether frozen']
weakness_name = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                 'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']

counter = 0
max_length = 0

for weakness in weakness_name:
    folder_path = abs_code_path + '\\' + weakness
    save_folder_path = abs_result_path + '\\' + weakness
    print(weakness)

    solidity_list = os.listdir(folder_path)

    for file_name in solidity_list:
        file_path = folder_path + '\\' + file_name
        save_file_path = save_folder_path + '\\' + file_name.split('.')[0]

        try:
            ast = solidity_to_ast(file_path)
            viz_code = ast_to_cfg(ast)
            length = extraction(viz_code)
            print(length)
            if length > max_length:
                max_length = length

            # counter += 1
            # if counter > 100:
            #     counter = 0
            #     break

        except Exception as e:
            continue




print(max_length)
print('done')