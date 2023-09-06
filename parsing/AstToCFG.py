from cfg_class import CFG, CFGNode, ID
from cfg_function import CreateCFG, ConditionalStatementProcessing, CreateFeature, FindingFunction, Traverse

dot_code = 'digraph G {\nnode[rx = 5, ry = 5, labelStyle = "font: 300 14px \'Helvetica Neue\', Helvetica"]\n'


# 솔리디티 코드에서 FuncionDefinition 단위로 CFG를 생성합니다.
def ast_to_cfg(ast):
    node_id = ID()
    cfg_list = [] # 생성된 CFG들을 담아두는 배열입니다.
    FindingFunction.finding_function(ast, cfg_list)

    for cfg in cfg_list.list:
        dot_code += cfg.cfg_to_dot()
    dot_code += '}'

    print(dot_code)
