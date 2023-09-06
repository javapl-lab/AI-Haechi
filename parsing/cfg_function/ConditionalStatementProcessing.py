# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 제어문 처리 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
def conditional_statement_processing(node, cfg=None):
    # Block 하위 리스트 순회
    for children in node['statements']:
        node_type = children['type']

        last_node = cfg.last_node()

        # 정의 처리부
        if node_type == 'ExpressionStatement':
            if last_node.node_name == 'Expression':
                traverse(children['expression'], cfg, cfg.last_node())
            else:
                Expression = CFGNode("Expression", id.get())

                (cfg.last_node()).add_successor(Expression)
                cfg.add_node(Expression)

                traverse(children['expression'], cfg, Expression)

        # 리턴 처리부
        elif node_type == 'Identifier':
            Reture = CFGNode("return", id.get())
            Reture.node_feature.append(" " + children['name'])
            cfg.last_node().add_successor(Reture)
            cfg.add_node(Reture)

        # If문 처리부
        elif node_type == 'IfStatement':
            Condition = CFGNode("Condition", id.get())
            (cfg.last_node()).add_successor(Condition)
            cfg.add_node(Condition)
            traverse(children['condition'], cfg, Condition)

            IfEnd = CFGNode("IfEnd", id.get())

            traverse(children['TrueBody'], cfg, Condition)
            if cfg.last_node().node_name != "return":
                cfg.last_node().add_successor(IfEnd)

            traverse(children['FalseBody'], cfg, Condition)
            if cfg.last_node().node_name != "return":
                cfg.last_node().add_successor(IfEnd)

            cfg.add_node(IfEnd)

        # While문 처리부
        elif node_type == 'WhileStatement':
            LoopCondition = CFGNode("LoopCondition", id.get())
            (cfg.last_node()).add_successor(LoopCondition)
            cfg.add_node(LoopCondition)
            traverse(children['condition'], cfg, LoopCondition)

            traverse(children['body'], cfg, LoopCondition)
            (cfg.last_node()).add_successor(LoopCondition)

            WhileEnd = CFGNode("WhileEnd", id.get())
            cfg.add_node(WhileEnd)
            LoopCondition.add_successor(WhileEnd)

        # For문 처리부
        elif node_type == 'ForStatement':
            Variable_Declaration = CFGNode("Variable Declaration", id.get())
            (cfg.last_node()).add_successor(Variable_Declaration)
            cfg.add_node(Variable_Declaration)
            traverse(children['initExpression'], cfg, Variable_Declaration)

            LoopCondition = CFGNode("LoopCondition", id.get())
            (cfg.last_node()).add_successor(LoopCondition)
            cfg.add_node(LoopCondition)
            traverse(children['conditionExpression'], cfg, LoopCondition)

            traverse(children['body'], cfg, LoopCondition)

            LoopExpression = CFGNode("LoopExpression", id.get())
            cfg.last_node().add_successor(LoopExpression)
            cfg.add_node(LoopExpression)
            traverse(children['loopExpression']['expression'], cfg, LoopExpression)
            (cfg.last_node()).add_successor(LoopCondition)

            ForEnd = CFGNode("ForEnd", id.get())
            cfg.add_node(ForEnd)
            LoopCondition.add_successor(ForEnd)