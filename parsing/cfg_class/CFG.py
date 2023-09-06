# 함수별 cfg
class CFG:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        """노드를 CFG에 추가합니다."""
        self.nodes.append(node)

    def last_node(self):
        return self.nodes[len(self.nodes) - 1]

    def cfg_to_dot(self):
        dot_code = ""

        for node in self.nodes:
            if node.node_name == "Condition" or node.node_name == "LoopCondition":
                dot_code += f'{node.node_id} [label = "{node.node_name}{" ".join(f"{feature}" for feature in node.node_feature)}" ];\n'
                dot_code += node.node_to_dot()
            elif node.node_feature:
                dot_code += f'{node.node_id} [label = "{node.node_name}{" ".join(f"{feature}" for feature in node.node_feature)}"];\n'
                dot_code += node.node_to_dot()
            else:
                dot_code += f"{node.node_id} [label = {node.node_name}];\n"
                dot_code += node.node_to_dot()

        return dot_code
