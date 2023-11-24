import os
from .SolidityToAST import solidity_to_ast
from Graph_generator_for_GNN.parsing.AstToCFG import ast_to_cfg
from Graph_generator_for_GNN.parsing.VizToDGL import viz_to_dgl
import graphviz


def generate(file_path, file_name):
    abs_result_path = os.path.abspath('../')
    if 'Graph_generator_for_GNN' in abs_result_path:
        abs_result_path = os.path.abspath('../result/')
    else:
        abs_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')

    #try:
    if not os.path.exists(abs_result_path):
        os.mkdir(abs_result_path)
        os.mkdir(os.path.join(abs_result_path, 'ast'))
        os.mkdir(os.path.join(abs_result_path, 'cfg'))
        os.mkdir(os.path.join(abs_result_path, 'preprocessed_ast'))

    ast = solidity_to_ast(file_path)
    viz_code = ast_to_cfg(ast)
    dgl_graph = viz_to_dgl(viz_code)
    abs_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')

    # file_name = file_name.split('.')[0]
    # cfg = graphviz.Source(viz_code)
    # cfg.format = 'png'
    # cfg.render(filename=os.path.join(abs_result_path, 'cfg/', file_name))

    return dgl_graph

    #except Exception as e:
        #print(str(e))