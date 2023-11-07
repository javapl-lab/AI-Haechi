from Graph_generator_for_GNN.parsing.cfg_class.CFG import CFG
from Graph_generator_for_GNN.parsing.cfg_class.Node import Node
from Graph_generator_for_GNN.parsing.cfg_class.GlobalCounter import GlobalCounter

node_counter = GlobalCounter()
function_counter = GlobalCounter()
variable_counter = GlobalCounter()
state_variable_counter = GlobalCounter()
function_dict = dict()
variable_dict = dict()
state_variable_dict = dict()


cfg_list = []

def test(node, cfg = None, pre_node = None, ifEnd_node = None):
    # If문 처리부
    node_id = node_counter.counter()
    condition_node = Node("Condition", node_id)
    pre_node.add_successor(condition_node.id)
    cfg.add_node(condition_node)
    traverse(node['condition'], cfg, condition_node)

    traverse(node['TrueBody'], cfg, condition_node)
    if cfg.last_node().name != "return":
        cfg.last_node().add_successor(ifEnd_node.id)

    if not node['FalseBody']:
        condition_node.add_successor(ifEnd_node.id)
    elif node['FalseBody']['type'] == 'IfStatement':
        test(node['FalseBody'], cfg, condition_node, ifEnd_node)
    else:
        traverse(node['FalseBody'], cfg, condition_node)
        if cfg.last_node().name != "return":
            cfg.last_node().add_successor(ifEnd_node.id)

# 노드를 받아와 해당 노드에서 feature를 문자열로 리턴
def create_feature(node):
    feature = ""

    if isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                feature += create_feature(item)
        return feature

    # 함수 표현
    elif node['type'] == 'FunctionCall':
        if node['expression']['type'] == 'Identifier':
            name = node['expression']['name']


            # 함수명 딕셔너리에 해당 키가 없으면 생성
            # if name not in function_dict:
            #     function_dict[name] = str(function_counter.counter())

            if name in function_dict:
                feature += "function" + function_dict[name] + ' ( '
            else:
                feature += name + ' ( '


            length = len(node['arguments'])
            for i in range(length):
                if i == 0:
                    feature += create_feature(node['arguments'][i])
                else:
                    feature += ' , ' + create_feature(node['arguments'][i])
            feature += ' ) '
            return feature

        # variable.push() 이런애들
        elif node['expression']['type'] == 'MemberAccess':
            feature = create_feature(node['expression']) + ' ( '
            length = len(node['arguments'])
            for i in range(length):
                if i == 0:
                    feature += create_feature(node['arguments'][i])
                else:
                    feature += ' , ' + create_feature(node['arguments'][i])
            feature += ' ) '
            return feature

    # 점
    elif node['type'] == 'MemberAccess':
        if node['memberName'] in function_dict:
            feature = create_feature(node['expression']) + ' . ' + "function" + function_dict[node['memberName']]
        else:
            feature = create_feature(node['expression']) + ' . ' + node['memberName']
        return feature

    # for문에서 변수 선언부의 자료형 제거 + '=' 생성
    elif node['type'] == 'VariableDeclarationStatement':
        # ast구조에 예외가 없다는 가정하에 진행한 내용
        feature = create_feature(node['variables']) + " = " + create_feature(node['initialValue'])
        return feature
    elif node['type'] == 'ElementaryTypeName':
        return feature

    # 중위식 표현
    elif node['type'] == 'BinaryOperation':
        feature = create_feature(node['left']) + ' ' + node['operator'] + ' ' + create_feature(node['right'])
        return feature

    # 증감 연산자 표현
    elif node['type'] == 'UnaryOperation':
        #전위
        if node['isPrefix'] == True:
            feature = node['operator'] + ' ' + create_feature(node['subExpression'])
        #후위
        elif node['isPrefix'] == False:
            feature =  create_feature(node['subExpression']) + ' ' + node['operator']
        return feature

    # 배열
    elif node['type'] == 'IndexAccess':
        feature = create_feature(node['base']) + ' [ ' + create_feature(node['index']) + ' ] '
        return feature


    for key, value in node.items():
        if isinstance(value, dict):
            feature += create_feature(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    feature += create_feature(item)

        elif isinstance(value, str):
            if key == 'name':
                if value in state_variable_dict:
                    feature += "state_variable" + state_variable_dict[value]
                elif value  in variable_dict:
                    feature += "variable" + variable_dict[value]
                else:
                    variable_dict[value] = str(variable_counter.counter())
                    feature += "variable" + variable_dict[value]
            elif key == 'number':
                if '.' in value:
                    feature += 'decimal'
                else:
                    feature += 'integer'
            elif key == 'operator':
                feature += value
            elif key == 'visibility':
                feature += value
            elif key == 'value':
                feature += 'string'
        elif isinstance(value, bool):
            if key == 'value':
                if value == True:
                    feature += 'True'
                elif value == False:
                    feature += 'False'

    return feature


def conditional_statement_processing(node, cfg=None):
    # Block 하위 리스트 순회
    for children in node['statements']:

        # return; 처리
        if children == None:
            return_node = Node("return", node_counter.counter())
            cfg.last_node().add_successor(return_node.id)
            cfg.add_node(return_node)
            return
        # break; 처리
        if children == ';':
            break_node = Node("break", node_counter.counter())
            cfg.last_node().add_successor(break_node.id)
            cfg.add_node(break_node)
            return


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

        # 선언 및 정의
        elif node_type == 'VariableDeclarationStatement':
            if children['initialValue']:
                if last_node.name == 'Expression':
                    traverse(children, cfg, cfg.last_node())
                else:
                    node_id = node_counter.counter()
                    expression_node = Node("Expression", node_id)

                    (cfg.last_node()).add_successor(expression_node.id)
                    cfg.add_node(expression_node)

                    traverse(children, cfg, expression_node)

        # 리턴 처리부
        elif (node_type == 'Identifier' or node_type == 'BinaryOperation'
              or node_type == 'NumberLiteral' or node_type == 'IndexAccess'
                or node_type == 'FunctionCall'):
            node_id = node_counter.counter()
            return_node = Node("return", node_id)
            return_node.feature.append("\n" + create_feature(children))
            cfg.last_node().add_successor(return_node.id)
            cfg.add_node(return_node)
        elif node_type == 'TupleExpression':
            return_node = Node("return", node_counter.counter())
            length = len(children['components'])
            for i in range(length):
                if i == 0:
                    return_node.feature.append(" " + create_feature(children['components'][i]))
                else:
                    return_node.feature.append(" , " + create_feature(children['components'][i]))
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

            # True
            if children['TrueBody']['type'] == 'Expression':
                node_id = node_counter.counter()
                expression_node = Node("Expression", node_id)

                (cfg.last_node()).add_successor(expression_node.id)
                cfg.add_node(expression_node)

                traverse(children['TrueBody'], cfg, expression_node)
            else:
                traverse(children['TrueBody'], cfg, condition_node)

            if cfg.last_node().name != "return":
                cfg.last_node().add_successor(ifEnd_node.id)

            # False
            if not children['FalseBody']:
                condition_node.add_successor(ifEnd_node.id)
            elif children['FalseBody']['type'] == 'IfStatement':
                test(children['FalseBody'], cfg, condition_node, ifEnd_node)
            elif children['FalseBody']['type'] == 'ExpressionStatement':
                node_id = node_counter.counter()
                expression_node = Node("Expression", node_id)

                (cfg.last_node()).add_successor(expression_node.id)
                cfg.add_node(expression_node)

                traverse(children['FalseBody'], cfg, expression_node)
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
            VariableDeclaration_node = Node("LoopVariable", node_id)
            (cfg.last_node()).add_successor(VariableDeclaration_node.id)
            cfg.add_node(VariableDeclaration_node)
            if children['initExpression'] == None:
                pass
            else:
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
    function_node.name = "Function"
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

        if node['name'] not in function_dict:
            function_dict[node['name']] = str(function_counter.counter())

        if isinstance(node['body'], list):
            pass
        else:
            cfg_list.append(create_cfg(node))
        return

    elif node_type == 'StateVariableDeclaration':
        for x in node['variables']:
            state_variable_dict[x['name']] = str(state_variable_counter.counter())
        return

    # 함수 외부에서 선언 및 선언 & 정의 / 이벤트 정의 등은 사용하지 않음
    elif (node_type == 'UsingForDeclaration'
          or node_type == 'InheritanceSpecifier' or node_type == 'EventDefinition'
          or node_type == 'PragmaDirective' or node_type == 'ModifierDefinition' or node_type == 'StructDefinition'):
        return
    # 연산자 + 단순 식별자(condition 단일값) + 점 연산자 + 배열
    elif (node_type == 'BinaryOperation' or node_type == 'UnaryOperation'
          or node_type == 'Identifier' or node_type == 'MemberAccess' or node_type == 'IndexAccess'):
        prev_node.feature.append("\n" + create_feature(node))

        return
    # for문 변수 선언부 or 변수에 값 할당
    elif node_type == 'VariableDeclarationStatement' or node_type == 'ExpressionStatement':
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