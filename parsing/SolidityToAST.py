from solidity_parser import parser
import re
import pprint


def solidityToAst(filename):
    try:
        solidity_file = open('./origin_sol_code/' + filename + '.txt', 'r')
        solidity_code = solidity_file.read()

        ast = parser.parse(solidity_code, loc=False)
        pprint.pprint(ast)
        ast_prepro = re.sub(r'[{}:\'"",\[\]]', '', str(ast))

        ast_file = open('./txt/ast/' + filename + '.txt', 'w+')
        ast_file.write(str(ast))

        ast_prepro_file = open('./txt/preprocessed_ast/' + filename + '.txt', 'w+')
        ast_prepro_file.write(ast_prepro)

        solidity_file.close()
        ast_file.close()
        ast_prepro_file.close()
    except(Exception,):
        print(str(Exception))

    return ast

    print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ solidityToAST done ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
