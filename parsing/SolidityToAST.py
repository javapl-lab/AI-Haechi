from solidity_parser import parser
import os
import re


def solidity_to_ast(filename):
    abstract_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ solidityToAST start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

    try:
        solidity_file = open('./origin_sol_code/' + filename + '.txt', 'r')
        solidity_code = solidity_file.read()

        ast = parser.parse(solidity_code, loc=False)
        ast_prepro = re.sub(r'[{}:\'"",\[\]]', '', str(ast))

        ast_file = open(os.path.join(abstract_result_path, 'ast/', filename), 'w+')
        ast_file.write(str(ast))

        ast_prepro_file = open(os.path.join(abstract_result_path, 'preprocessed_ast/', filename), 'w+')
        ast_prepro_file.write(ast_prepro)

        solidity_file.close()
        ast_file.close()
        ast_prepro_file.close()

        print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ solidityToAST done ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

        return ast
    except Exception as e:
        print(str(e))
