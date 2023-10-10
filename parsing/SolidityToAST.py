from solidity_parser import parser
import os
import re


def solidity_to_ast(file_path):
    abs_result_path = os.path.abspath('../')
    if 'Graph_generator_for_GNN' in abs_result_path:
        abs_result_path = os.path.abspath('../result/')
    else:
        abs_result_path = os.path.abspath('../Graph_generator_for_GNN/result/')

    print('으갸갸갹:', abs_result_path)

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ SolidityToAST start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

    try:
        solidity_file = open(file_path, 'r')
        solidity_code = solidity_file.read()

        ast = parser.parse(solidity_code, loc=False)

        solidity_file.close()
        print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ SolidityToAST done ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')

        return ast
    except Exception as e:
        print(str(e))
