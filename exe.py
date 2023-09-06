import embedding
from parsing import SolidityToAST
from parsing import AstToCFG

filename = 'if_code'
ast = SolidityToAST.solidityToAst(filename)
AstToCFG(ast)
