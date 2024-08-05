import os
import sys
sys.path.insert(0, '/workspace/sku3343/heesung')
import dgl
from Generator import generate
  
file_path = os.path.abspath('../sku3343/dataset/solidity/')
result_path = os.path.abspath('../sku3343/dataset/')

weakness_list = ['block number dependency', 'dangerous delegatecall', 'ether frozen', 'ether strict equality',
                    'integer overflow', 'reentrancy', 'timestamp dependency', 'unchecked external call']
select_weakness = ['dangerous delegatecall']
success_count = 0
fail_count = 0

for weakness in select_weakness:
    folder_path = file_path + '/' + weakness
    solidity_list = os.listdir(folder_path)
    for file_name in solidity_list:
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        print('now...', file_name)

        try:
            g = generate(folder_path + '/', file_name, result_path)
            dgl.save_graphs(result_path + '/dgl_graph/{0}/{1}'.format(weakness, str(file_name[:-4])), g)
            success_count += 1

        except Exception as e:
            fail_count += 1
            print(file_name + ": " + str(e))
            print('success:', success_count)
            print('fail:', fail_count)
            continue
            
        print('success:', success_count)
        print('fail:', fail_count)

# g = generate(file_path + '/ether frozen/', '0.sol', result_path)
# print(g)
# # print(g.ndata['feat'])
# dgl.save_graphs(result_path + '/dgl_graph/{0}/{1}'.format('ether frozen', 0), g)