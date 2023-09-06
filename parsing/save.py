import os
import AstToCFG
from solidity_parser import parser

solidity_code = open('../txt/ast/ast0.txt').read()

ast = parser.parse(solidity_code)
cfg_list = AstToCFG.CFGList()
AstToCFG.traverse(ast, cfg_list)

dot_code = 'digraph G {\n'
for cfg in cfg_list.list:
    dot_code += cfg.cfg_to_dot()
dot_code += '}'

file_path = 'cfg/txt/'
file_name = 'dagre'
file_ext = '.txt'

file_num = 0
while os.path.exists(file_path + file_name + str(file_num) + file_ext):
    file_num += 1


print(file_path + file_name + str(file_num) + file_ext)
dagre_file = open(file_path + file_name + str(file_num) + file_ext, 'w+')
dagre_file.write(dot_code)

dagre_file.close()