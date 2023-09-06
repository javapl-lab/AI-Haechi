def create_cfg(node):
    cfg = CFG()
    Function = CFGNode("Function", id.get())
    cfg.add_node(Function)

    # 매개변수에 대한 내용은 추가할거면 여기에

    traverse(node['body'], cfg, Function)

    # FunctionEnd
    FunctionEnd = CFGNode("FunctionEnd", id.get())
    for node in cfg.nodes:
        if not node.successors:
            node.add_successor(FunctionEnd)
    cfg.add_node(FunctionEnd)
    return cfg