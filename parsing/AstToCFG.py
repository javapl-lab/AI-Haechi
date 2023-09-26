from Graph_generator_for_GNN.parsing.cfg_class.CFG import CFG
from Graph_generator_for_GNN.parsing.cfg_class.Node import Node
from Graph_generator_for_GNN.parsing.cfg_class.GlobalCounter import GlobalCounter

global_counter = GlobalCounter()
cfg_list = []


# 노드를 받아와 해당 노드에서 feature를 문자열로 리턴
def create_feature(node):
    feature = ""
    for key, value in node.items():
        if isinstance(value, dict):
            feature += create_feature(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    feature += create_feature(item)

        elif isinstance(value, str):
            if key == 'name':
                feature += value + ' '
            if key == 'operator':
                feature += value + ' '
            if key == 'number':
                feature += value + ' '
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
                expression_node = Node("Expression", global_counter.counter())

                (cfg.last_node()).add_successor(expression_node.id)
                cfg.add_node(expression_node)

                traverse(children['expression'], cfg, expression_node)

        # 리턴 처리부
        elif node_type == 'Identifier':
            return_node = Node("return", global_counter.counter())
            return_node.feature.append(" " + children['name'])
            cfg.last_node().add_successor(return_node.id)
            cfg.add_node(return_node)

        # If문 처리부
        elif node_type == 'IfStatement':
            condition_node = Node("Condition", global_counter.counter())
            (cfg.last_node()).add_successor(condition_node.id)
            cfg.add_node(condition_node)
            traverse(children['condition'], cfg, condition_node)

            ifEnd_node = Node("IfEnd", global_counter.counter())

            traverse(children['TrueBody'], cfg, condition_node)
            if cfg.last_node().name != "return":
                cfg.last_node().add_successor(ifEnd_node.id)

            traverse(children['FalseBody'], cfg, condition_node)
            if cfg.last_node().name != "return":
                cfg.last_node().add_successor(ifEnd_node.id)

            cfg.add_node(ifEnd_node)

        # While문 처리부
        elif node_type == 'WhileStatement':
            loopCondition_node = Node("LoopCondition", global_counter.counter())
            (cfg.last_node()).add_successor(loopCondition_node.id)
            cfg.add_node(loopCondition_node)
            traverse(children['condition'], cfg, loopCondition_node)

            traverse(children['body'], cfg, loopCondition_node)
            (cfg.last_node()).add_successor(loopCondition_node.id)

            whileEnd_node = Node("WhileEnd", global_counter.counter())
            cfg.add_node(whileEnd_node)
            loopCondition_node.add_successor(whileEnd_node.id)

        # For문 처리부
        elif node_type == 'ForStatement':
            VariableDeclaration_node = Node("Variable Declaration", global_counter.counter())
            (cfg.last_node()).add_successor(VariableDeclaration_node.id)
            cfg.add_node(VariableDeclaration_node)
            traverse(children['initExpression'], cfg, VariableDeclaration_node)

            loopCondition_node = Node("LoopCondition", global_counter.counter())
            (cfg.last_node()).add_successor(loopCondition_node.id)
            cfg.add_node(loopCondition_node)
            traverse(children['conditionExpression'], cfg, loopCondition_node)

            traverse(children['body'], cfg, loopCondition_node)

            loopExpression_node = Node("LoopExpression", global_counter.counter())
            cfg.last_node().add_successor(loopExpression_node.id)
            cfg.add_node(loopExpression_node)
            traverse(children['loopExpression']['expression'], cfg, loopExpression_node)
            (cfg.last_node()).add_successor(loopCondition_node.id)

            forEnd_node = Node("ForEnd", global_counter.counter())
            cfg.add_node(forEnd_node)
            loopCondition_node.add_successor(forEnd_node.id)


def create_cfg(node):
    cfg = CFG()
    function_node = Node("Function", global_counter.counter())
    cfg.add_node(function_node)

    # 매개변수에 대한 내용은 추가할거면 여기에

    traverse(node['body'], cfg, function_node)

    # FunctionEnd
    functionend_node = Node("FunctionEnd", global_counter.counter())
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
        cfg_list.append(create_cfg(node))
        return
    # 함수 외부에서 선언 및 선언 & 정의 / 이벤트 정의 등은 사용하지 않음
    elif node_type == 'StateVariableDeclaration' or node_type == 'UsingForDeclaration' or node_type == 'InheritanceSpecifier' or node_type == 'EventDefinition':
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
        current_node = Node(node_type, global_counter.counter())
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
    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ast_to_cfg start ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    traverse(ast)

    viz_code = 'digraph G {\nnode[shape=box, style=rounded, fontname="Sans"]\n'

    for cfg in cfg_list:
        viz_code += cfg.cfg_to_dot()
    viz_code += '}'

    print(' ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ast_to_cfg done ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ ')
    return viz_code
