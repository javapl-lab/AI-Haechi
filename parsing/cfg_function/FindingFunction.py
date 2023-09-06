# 함수 탐색
def finding_function(node, cfg_list=None):
    node_type = node.get('type')

    if node_type == 'FunctionDefinition':
        cfg_list.add_list(create_cfg(node))
        return

    if not node_type:
        return

    for key, value in node.items():
        if isinstance(value, dict):
            Finding_Function(value, cfg_list)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    Finding_Function(item, cfg_list)