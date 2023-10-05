import os
from .SolidityToAST import solidity_to_ast
from Graph_generator_for_GNN.parsing.AstToCFG import ast_to_cfg
from Graph_generator_for_GNN.parsing.VizToDGL import viz_to_dgl
import graphviz


def generate(file_name):
    abstract_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')
    try:
        if not os.path.exists(abstract_result_path):
            os.mkdir(abstract_result_path)
            print()
            os.mkdir(os.path.join(abstract_result_path, 'ast'))
            os.mkdir(os.path.join(abstract_result_path, 'cfg'))
            os.mkdir(os.path.join(abstract_result_path, 'cfg_img'))
            os.mkdir(os.path.join(abstract_result_path, 'preprocessed_ast'))
    except Exception as e:
        print(str(e))

    ast = solidity_to_ast(file_name)
    viz_code = ast_to_cfg(ast)
    viz_to_dgl(viz_code)
    abstract_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')

    cfg = graphviz.Source(viz_code)
    cfg.format = 'png'
    cfg.render(filename=os.path.join(abstract_result_path, 'cfg_img/', file_name))
    cfg.view()

    return
