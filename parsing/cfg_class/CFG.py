
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
        viz_code = ""

        for node in self.nodes:
            if node.name == "Condition" or node.name == "LoopCondition":
                viz_code += f'{node.id} [label = "{node.name}{" ".join(f"{feature}" for feature in node.feature)}", shape = diamond];\n'
                viz_code += node.node_to_dot()
            elif node.feature:
                viz_code += f'{node.id} [label = "{node.name}{" ".join(f"{feature}" for feature in node.feature)}"];\n'
                viz_code += node.node_to_dot()
            else:
                viz_code += f"{node.id} [label = {node.name}];\n"
                viz_code += node.node_to_dot()

                #시작적인 복잡함 해결
                if node.name == "WhileEnd" or node.name == "ForEnd":
                    viz_code += f'{{rank=same; {str(node.id)}; {str(node.id - 1)}}}\n'

        return viz_code