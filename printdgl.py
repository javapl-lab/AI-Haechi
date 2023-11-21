import os
import pickle

list1 = os.listdir('../Graph_generator_for_GNN/result/dgl_graph/block number dependency')

total = 0
fail = 0

for x in list1:

    with open(os.path.abspath('../Graph_generator_for_GNN/result/dgl_graph/block number dependency')+'\\'+ x, 'rb') as f:
        data = pickle.load(f)
    print(x, '-------------------------')
    print(data)
    total += 1
    if data is None:
        fail += 1


print(fail)
print(total)