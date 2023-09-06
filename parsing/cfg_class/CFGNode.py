# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ CFG의 노드 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
class CFGNode:
    def __init__(self, node_name, node_id):
        self.node_name = node_name
        self.node_id = node_id
        self.successors = []
        self.node_feature = []

    def add_successor(self, successor):
        """연결된 후속 노드를 추가합니다."""
        self.successors.append(successor)

    def node_to_dot(self):
        dot_code = ""

        if len(self.successors) > 1:
            dot_code += f'{self.node_id} -> {self.successors[0].node_id} [label = "true" labelStyle = "fill: #77f; font-weight: bold;"];\n'
            dot_code += f'{self.node_id} -> {self.successors[1].node_id} [label = "false" labelStyle = "fill: #f77; font-weight: bold;"];\n'
        elif len(self.successors) == 1:
            dot_code += f'{self.node_id} -> {self.successors[0].node_id};\n'

        return dot_code
