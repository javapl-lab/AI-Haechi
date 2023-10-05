import re
import dgl
import torch as th


def viz_to_dgl(viz_code):
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ viz_to_dgl start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    dgl_U = []
    dgl_V = []
    viz_edges = re.findall(r'\d+ -> \d+', viz_code)
    for i in viz_edges:
        dgl_U.append(int(i.split()[0]))
        dgl_V.append(int(i.split()[2]))

    tensor_U = th.tensor(dgl_U)
    tensor_V = th.tensor(dgl_V)
    graph = dgl.graph((tensor_U, tensor_V))
    print('u:', tensor_U)
    print('v:', tensor_V)
    print(graph)

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ viz_to_dgl end ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

