import re
import dgl
import numpy
import torch as th
from torch.nn.utils.rnn import pad_sequence

node_list = ['Block', 'Condition', 'return', 'IfEnd', 'Expression', 
             'FunctionEnd', 'LoopVariable', 'LoopExpression', 'ForEnd', 'break', 
             'WhileEnd', 'throw']

def viz_to_dgl(viz_code, normalization_dict):
    # print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    node_dict = dict()
    edge_list = []
    src_list = []
    dst_list = []
    feature_dict = dict()
    feature_list = []
    node_id = 0
    graph_data = {}
    
    #첫 노드를 Function에서 Block으로 변경
    viz_code = (viz_code.strip().split('\n'))[3:]
    feature_dict[str(node_id)] = feature_list
    node_dict[str(node_id)] = 'Block'
    
    # 정규식을 사용해 viz_code로 부터 데이터 추출
    for line in viz_code:
        line = re.sub(r'[,\}\{;\"]', '', line)
        
        # node_dict 생성
        # n [label = node_name] 형태
        if 'label' in line and '->' not in line:
            node_id = line.split()[0]
            # 새로운 노드를 만나면 특징 리스트 초기화
            feature_list = []
            feature_dict[node_id] = feature_list
            node_dict[node_id] = re.sub(r"[^a-zA-Z]", "", line.split()[3])
            
            # if re.sub(r"[^a-zA-Z]", "", line.split()[3]) not in node_list:
            #     print(re.sub(r"[^a-zA-Z]", "", line.split()[3]),"추가됨")
            #     node_list.append(re.sub(r"[^a-zA-Z]", "", line.split()[3]))
        
        # edge_list 생성
        elif '->' in line:
            # n -> m [label = true fontcolor=blue] 형태
            if 'label' in line: 
                edge_list.append(line.split()[5])
                src_list.append(int(line.split()[0]))
                dst_list.append(int(line.split()[2]))
            # n -> m 형태
            else:
                edge_list.append('normal')
                src_list.append(int(line.split()[0]))
                dst_list.append(int(line.split()[2]))

        # feature_dict 생성
        else:
            if node_dict[node_id] != "ForEnd":
                if line.count('[') < line.count(']'):
                    line = line[:-1]
                if "shape" in line:
                    line = line[:-16]
                
                line = line.split(' ')
                for token in line:
                    if token != '':
                        if token in normalization_dict:
                            feature_list.append(normalization_dict[token])
                        else:
                            feature_list.append(normalization_dict["OOV"])
                feature_dict[node_id] = feature_list
                
    # print("현재 노드 리스트:", node_list)
    #print("feature_dict:", feature_dict)
    
    empty_node_list = []
    # 모든 노드 타입을 가지도록 맨 마지막에 빈 노드 추가
    for node in node_list:
        if node not in node_dict.values():
            # print(node, "추가")
            empty_node_list.append(node)
                
    src_list = numpy.array(src_list)
    dst_list = numpy.array(dst_list)
    
    # graph_data 생성
    for edge, src, dst in zip(edge_list, src_list, dst_list):
        key = node_dict[str(src)], edge, node_dict[str(dst)]
        if key not in graph_data:
            graph_data[key] = (th.tensor([src]), th.tensor([dst]))
        else:
            graph_data[key] = (th.cat((graph_data[key][0], th.tensor([src]))), th.cat((graph_data[key][1], th.tensor([dst]))))
    for empty_node in empty_node_list:
        graph_data[empty_node, 'normal', empty_node] = (th.tensor([0]), th.tensor([1]))
    
    # feature tensor 생성
    tensor = th.zeros(int(node_id) + 1, 128)
    for key in feature_dict.keys():
        feature_value = feature_dict[key]
        # feature를 길이 128의 배열로 변환
        feature_value = numpy.pad(feature_value, (0, max(0, 128 - len(feature_value))))[:128]
        tensor[int(key)] = th.tensor(feature_value)
    
    g = dgl.heterograph(graph_data)
    
    # node_list를 순회하면서 각 노드별 특징 텐서 생성
    for node in node_list:
        # print("ㅡㅡㅡㅡㅡ", node, "ㅡㅡㅡㅡㅡ")
        feature_tensor = th.zeros(len(g.nodes(node)), 128) 
        for key in feature_dict.keys():
            if node_dict[key] == node:
                feature_tensor[int(key)] = tensor[int(key)]
        
        g.nodes[node].data['feat'] = feature_tensor
        #print(node, "노드 길이: ",len(feature_tensor))

    # print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL end ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    
    return g