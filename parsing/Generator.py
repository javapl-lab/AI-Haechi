import os
import sys
sys.path.insert(0, '/workspace/sku3343/heesung')
from parsing.SolidityToAST import solidity_to_ast
from parsing.AstToCFG import ast_to_cfg
from parsing.VizToDGL import viz_to_dgl
# import vizgraph

def generate(file_path, file_name, result_path):
    # if not os.path.exists(result_path):
    #     os.mkdir(result_path)
    #     os.mkdir(os.path.join(result_path, 'ast'))
    #     os.mkdir(os.path.join(result_path, 'cfg'))
    #     os.mkdir(os.path.join(result_path, 'preprocessed_ast'))

    ast = solidity_to_ast(os.path.join(file_path, file_name))
    viz_code = ast_to_cfg(ast)
    
    # return viz_code # 단어 임베딩을 위한 빈도수 체크 진행 시 viz_code만 반환

    normalization_dict = eval(open(result_path + '/Normalization.txt', 'r').read())
    dgl_graph = viz_to_dgl(viz_code, normalization_dict)

    # file_name = file_name.split('.')[0]
    # cfg = graphviz.Source(viz_code)
    # cfg.format = 'png'
    # cfg.render(filename=os.path.join(result_path, 'cfg/', file_name))
    
    return dgl_graph
