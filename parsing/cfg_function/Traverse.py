# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 순회 시작 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def traverse(node, cfg=None, prev_node=None):
    node_type = node.get('type')

    if not node_type:
        return
    # 연산자
    elif node_type == 'BinaryOperation' or node_type == 'UnaryOperation':
        prev_node.node_feature.append("\n" + create_feature(node))
        return
    # for문 변수 선언부
    elif node_type == 'VariableDeclarationStatement':
        prev_node.node_feature.append("\n" + create_feature(node))
        return

    #
    elif node_type == 'FunctionCall':
        prev_node.node_feature.append("\n" + create_feature(node))
        return

    current_node = CFGNode(node['type'], id.get())
    cfg.add_node(current_node)

    if prev_node:
        prev_node.add_successor(current_node)

    if node_type == 'Block':
        ConditionalStatementProcessing(node, cfg)
        return

    for key, value in node.items():
        if isinstance(value, dict):
            traverse(value, cfg, current_node)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    traverse(item, cfg, current_node)

    return
