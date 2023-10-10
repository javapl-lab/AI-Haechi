from Graph_generator_for_GNN.parsing.cfg_class.CFG import CFG
from Graph_generator_for_GNN.parsing.cfg_class.Node import Node
from Graph_generator_for_GNN.parsing.cfg_class.GlobalCounter import GlobalCounter

node_counter = GlobalCounter()
function_counter = GlobalCounter()
variable_counter = GlobalCounter()
function_dict = dict()
variable_dict = dict()

cfg_list = []


# 노드를 받아와 해당 노드에서 feature를 문자열로 리턴
def create_feature(node):
    node_type = node['type']
    if node_type == 'FunctionCall':
        if node['expression']['type'] == 'Identifier':
            name = node['expression']['name']
            # 함수명 딕셔너리에 해당 키가 없으면 생성
            if name not in function_dict:
                function_dict[name] = str(function_counter.counter())

    feature = ""
    operator = ""
    for key, value in node.items():
        if isinstance(value, dict):
            # 변수 할당부분 특징 추가용
            if key == 'right':
                feature += operator + ' '
            feature += create_feature(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    feature += create_feature(item)

        elif isinstance(value, str):
            if key == 'name':
                if value in function_dict:
                    feature += "function" + function_dict[value] + ' '
                elif value in variable_dict:
                    feature += "variable" + variable_dict[value] + ' '
                elif value not in variable_dict:
                    variable_dict[value] = str(variable_counter.counter())
                    feature += "variable" + variable_dict[value] + ' '
            if key == 'number':
                if '.' in value:
                    feature += 'decimal' + ' '
                else:
                    feature += 'integer' + ' '
            if key == 'operator':
                operator = value
            if key == 'visibility':
                feature += value + ' '
        elif isinstance(value, bool):
            if key == 'isPrefix':
                if value:
                    feature += "Perfix Operator"
                else:
                    feature += "Postfix Operator"
            '''다른 추가적인 정보 담아야함'''

    return feature


def conditional_statement_processing(node, cfg=None):
    # Block 하위 리스트 순회
    for children in node['statements']:
        node_type = children['type']

        last_node = cfg.last_node()

        # 정의 처리부
        if node_type == 'ExpressionStatement':
            if last_node.name == 'Expression':
                traverse(children['expression'], cfg, cfg.last_node())
            else:
                node_id = node_counter.counter()
                expression_node = Node("Expression", node_id)

                (cfg.last_node()).add_successor(expression_node.id)
                cfg.add_node(expression_node)

                traverse(children['expression'], cfg, expression_node)

        # 리턴 처리부
        elif node_type == 'Identifier' or node_type == 'BinaryOperation' or node_type == 'NumberLiteral':
            node_id = node_counter.counter()
            return_node = Node("return", node_id)
            return_node.feature.append(" " + create_feature(node))
            cfg.last_node().add_successor(return_node.id)
            cfg.add_node(return_node)

        # If문 처리부
        elif node_type == 'IfStatement':
            node_id = node_counter.counter()
            condition_node = Node("Condition", node_id)
            (cfg.last_node()).add_successor(condition_node.id)
            cfg.add_node(condition_node)
            traverse(children['condition'], cfg, condition_node)

            node_id = node_counter.counter()
            ifEnd_node = Node("IfEnd", node_id)

            traverse(children['TrueBody'], cfg, condition_node)
            if cfg.last_node().name != "return":
                cfg.last_node().add_successor(ifEnd_node.id)

            if not children['FalseBody']:
                condition_node.add_successor(ifEnd_node.id)
            else:
                traverse(children['FalseBody'], cfg, condition_node)
                if not children['FalseBody']:
                    condition_node.add_successor(ifEnd_node.id)
                else:
                    traverse(children['FalseBody'], cfg, condition_node)
                    if cfg.last_node().name != "return":
                        cfg.last_node().add_successor(ifEnd_node.id)

            cfg.add_node(ifEnd_node)

        # While문 처리부
        elif node_type == 'WhileStatement':
            node_id = node_counter.counter()
            loopCondition_node = Node("LoopCondition", node_id)
            (cfg.last_node()).add_successor(loopCondition_node.id)
            cfg.add_node(loopCondition_node)
            traverse(children['condition'], cfg, loopCondition_node)

            traverse(children['body'], cfg, loopCondition_node)
            (cfg.last_node()).add_successor(loopCondition_node.id)

            node_id = node_counter.counter()
            whileEnd_node = Node("WhileEnd", node_id)
            cfg.add_node(whileEnd_node)
            loopCondition_node.add_successor(whileEnd_node.id)

        # For문 처리부
        elif node_type == 'ForStatement':
            node_id = node_counter.counter()
            VariableDeclaration_node = Node("Variable Declaration", node_id)
            (cfg.last_node()).add_successor(VariableDeclaration_node.id)
            cfg.add_node(VariableDeclaration_node)
            traverse(children['initExpression'], cfg, VariableDeclaration_node)

            node_id = node_counter.counter()
            loopCondition_node = Node("LoopCondition", node_id)
            (cfg.last_node()).add_successor(loopCondition_node.id)
            cfg.add_node(loopCondition_node)
            traverse(children['conditionExpression'], cfg, loopCondition_node)

            traverse(children['body'], cfg, loopCondition_node)

            node_id = node_counter.counter()
            loopExpression_node = Node("LoopExpression", node_id)
            cfg.last_node().add_successor(loopExpression_node.id)
            cfg.add_node(loopExpression_node)
            traverse(children['loopExpression']['expression'], cfg, loopExpression_node)
            (cfg.last_node()).add_successor(loopCondition_node.id)

            node_id = node_counter.counter()
            forEnd_node = Node("ForEnd", node_id)
            cfg.add_node(forEnd_node)
            loopCondition_node.add_successor(forEnd_node.id)


def create_cfg(node):
    cfg = CFG()
    node_id = node_counter.counter()
    function_node = Node("Function", node_id)
    cfg.add_node(function_node)

    # 매개변수에 대한 내용은 추가할거면 여기에

    traverse(node['body'], cfg, function_node)

    # FunctionEnd
    node_id = node_counter.counter()
    functionend_node = Node("FunctionEnd", node_id)
    for node in cfg.nodes:
        if not node.successors:
            node.add_successor(functionend_node.id)
    cfg.add_node(functionend_node)
    return cfg


def traverse(node, cfg=None, prev_node=None):
    node_type = node.get('type')

    if not node_type:   
        return
    # 함수선언부
    elif node_type == 'FunctionDefinition':
        if isinstance(node['body'], list):
            pass
        else:
            cfg_list.append(create_cfg(node))
        return
    # 함수 외부에서 선언 및 선언 & 정의 / 이벤트 정의 등은 사용하지 않음
    elif node_type == 'StateVariableDeclaration' or node_type == 'UsingForDeclaration' or node_type == 'InheritanceSpecifier' or node_type == 'EventDefinition'  or node_type == 'PragmaDirective' or node_type == 'ModifierDefinition':
        return
    # 연산자
    elif node_type == 'BinaryOperation' or node_type == 'UnaryOperation':
        prev_node.feature.append("\n" + create_feature(node))
        return
    # for문 변수 선언부
    elif node_type == 'VariableDeclarationStatement':
        prev_node.feature.append("\n" + create_feature(node))
        return
    # FunctionCall
    elif node_type == 'FunctionCall':
        prev_node.feature.append("\n" + create_feature(node))
        return

    if node_type == 'SourceUnit' or node_type == 'ContractDefinition':
        current_node = None
    else:
        node_id = node_counter.counter()
        current_node = Node(node_type, node_id)
        cfg.add_node(current_node)

    if prev_node:
        prev_node.add_successor(current_node.id)

    if node_type == 'Block':
        conditional_statement_processing(node, cfg)
        return

    for key, value in node.items():
        if isinstance(value, dict):
            traverse(value, cfg, current_node)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    traverse(item, cfg, current_node)


##################################################################################################################

def ast_to_cfg(ast):
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ AstToCFG start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    traverse(ast)

    viz_code = 'digraph G {\nnode[shape=box, style=rounded, fontname="Sans"]\n'

    for cfg in cfg_list:
        viz_code += cfg.cfg_to_dot()
    viz_code += '}'

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ AstToCFG done ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    return viz_code
