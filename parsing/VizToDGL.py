import re
import dgl
import torch as th


def viz_to_dgl(viz_code):
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    dgl_U, dgl_V = [], []
    node_dict = dict()
    edge_dict = dict()
    feature_dict = dict()
    feature_list = []
    node_id = 0

    viz_edges = re.findall(r'\d+ -> \d+', viz_code)
    for i in viz_edges:
        dgl_U.append(int(i.split()[0]))
        dgl_V.append(int(i.split()[2]))
    tensor_U = th.tensor(dgl_U)
    tensor_V = th.tensor(dgl_V)

    viz_code = (viz_code.strip().split('\n'))
    print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
    for line in viz_code:
        print(line)
        if re.findall(r'\d+ \[label = ', line):
            node_id = line.split()[0]
            feature_list = []
            if '->' in line:
                edge_dict[line.split()[0] + ' -> ' + line.split()[2]] = re.sub(r"[^a-zA-Z]", "", line.split()[5])
            else:
                node_dict[line.split()[0]] = re.sub(r"[^a-zA-Z]", "", line.split()[3])
        elif '{' not in line and '[' not in line and '=' in line or '+' in line or '-':
            if ']' in line:
                line = ' '.join(line.split()[:-1])
            if 'shape' in line:
                line = ' '.join(line.split()[:-3])
            feature_list.append(line)
            feature_dict[node_id] = feature_list

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

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ VizToDGL end ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

