import os.path
import re
import dgl
import json
import torch as th


def viz_to_dgl(viz_code):
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    print(viz_code)
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    dgl_U, dgl_V = [], []
    node_dict = dict()
    edge_dict = dict()
    feature_dict = dict()
    feature_list = []
    node_id = 0
    normalization = open(os.path.abspath('../Graph_generator_for_GNN/result/embedding/Normalization.txt'), 'r').read()
    normalization_dict = eval(normalization)

    viz_edges = re.findall(r'\d+ -> \d+', viz_code)
    for i in viz_edges:
        dgl_U.append(int(i.split()[0]))
        dgl_V.append(int(i.split()[2]))
    tensor_U = th.tensor(dgl_U)
    tensor_V = th.tensor(dgl_V)

    viz_code = (viz_code.strip().split('\n'))
    # 정규식을 사용해 viz_code로 부터 데이터 추출
    for line in viz_code:
        # node_dict를 생성
        if re.findall(r'\d+ \[label = ', line):
            node_id = line.split()[0]
            feature_list = []
            if ' -> ' not in line:
                node_dict[line.split()[0]] = re.sub(r"[^a-zA-Z]", "", line.split()[3])
                
        # edge_dict를 생성
        if '->' in line:
            if 'label' in line:
                edge_dict[line.split()[0] + ' -> ' + line.split()[2]] = re.sub(r"[^a-zA-Z]", "", line.split()[5])
            else:
                print('edge: ', line)
                edge_dict[line.split()[0] + ' -> ' + re.sub(';', '', line.split()[2])] = 'normal'
                
        # feature_dict를 생성
        if '{' not in line and '[' not in line and '->' not in line:
            pattern = re.compile(r'"(.*?);')
            line = re.sub(pattern, '', line)
            print('-----------------')
            print('first filtered line: ' + line)
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
            print(feature_list)
            feature_dict[node_id] = feature_list

    # 맨 마지막 키인 '}'를 딕셔너리에서 제거
    last_key = list(feature_dict.keys())[-1]
    del feature_dict[last_key]

    # 가장 긴 특징의 길이
    max_feature_length = 0
    for key in feature_dict:
        if max_feature_length < len(feature_dict[key]):
            max_feature_length = len(feature_dict[key])
    print('max_feature_length:', max_feature_length)

    print('node_dict:', node_dict)
    print('edge_dict:', edge_dict)
    print('feature_dict:', feature_dict)

    graph_data = {
        ('Function', 'normal', 'Block'): (th.tensor([0]), th.tensor([1])),
        ('Block', 'normal', 'Expression'): (th.tensor([1]), th.tensor([2])),
        ('Expression', 'normal', 'Condition'): (th.tensor([2]), th.tensor([3])),
        ('Condition', 'true', 'Block'): (th.tensor([3]), th.tensor([5])),
        ('Condition', 'false', 'Block'): (th.tensor([3]), th.tensor([8])),
        ('Block', 'normal', 'Expression'): (th.tensor([5]), th.tensor([6])),
        ('Expression', 'normal', 'return'): (th.tensor([6]), th.tensor([7])),
        ('return', 'normal', 'FunctionEnd'): (th.tensor([7]), th.tensor([11])),
        ('Block', 'normal', 'Expression'): (th.tensor([8]), th.tensor([9])),
        ('Expression', 'normal', 'IfEnd'): (th.tensor([9]), th.tensor([4])),
        ('IfEnd', 'normal', 'Expression'): (th.tensor([4]), th.tensor([10])),
        ('Expression', 'normal', 'FunctionEnd'): (th.tensor([10]), th.tensor([11])),
    }
    graph = dgl.heterograph(graph_data)

    graph.nodes['Expression'].data['test'] = th.ones(graph.num_nodes('Expression'), 6)
    print(graph.nodes['Expression'].data['test'])

    graph.nodes['Expression'].data['test'][2][0] = 1.1
    graph.nodes['Expression'].data['test'][2][1] = 1.2
    graph.nodes['Expression'].data['test'][2][2] = 1.3
    graph.nodes['Expression'].data['test'][2][3] = 1.4

    graph.nodes['Expression'].data['test'][10][0] = 1.95

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL end ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')


