import os.path
import re
import dgl
import json
import torch as th


def viz_to_dgl(viz_code):
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    # print(viz_code)
    # print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
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
    tensor_U = th.tensor(dgl_U)
    tensor_V = th.tensor(dgl_V)

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
            # print('-----------------')
            # print('filtered line: ' + line)
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
            #print(feature_list)
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

    print('node_dict:', node_dict)
    print('edge_list:', edge_list)
    print('feature_dict:', feature_dict)
    print('max_feature_length:', max_feature_length)

    ###################################################################################################################

    tuple_list = []
    objects = []
    class EdgeClass:
        def __init__(self, edge):
            self.u_list = []
            self.v_list = []
            self.edge = edge

    for u, edge, v in edge_list:
        if (node_dict[u], edge, node_dict[v]) not in tuple_list:
            tuple_list.append((node_dict[u], edge, node_dict[v]))

            obj = EdgeClass((node_dict[u], edge, node_dict[v]))
            objects.append(obj)
            obj.u_list.append(int(u))
            obj.v_list.append(int(v))
        else:
            for obj in objects:
                if obj.edge == (node_dict[u], edge, node_dict[v]):
                    obj.u_list.append(int(u))
                    obj.v_list.append(int(v))

    # objects 리스트에는 엣지클래스의 객체들이 담겨 있다.
    # 객체들은 각각 튜플, 그리고 해당 튜플로 이루어진 u,v쌍을 리스트로 지니고 있다.
    ###################################################################################################################

    graph_data = {}

    for obj in objects:
        graph_data[obj.edge] = (th.tensor(obj.u_list), th.tensor(obj.v_list))

    graph = dgl.heterograph(graph_data)

    # 그래프 생성
    ###################################################################################################################

    graph.nodes['Expression'].data['expression'] = th.ones(graph.num_nodes('Expression'), max_feature_length)


    for key, values in feature_dict.items():
        for i in range(len(values)):
            graph.nodes['Expression'].data['expression'][int(key)][i] = values[i]

    print(graph)

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL end ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

    
    # expression노드에 특징 삽입
    ###################################################################################################################
