# cfg의 각 노드들
class Node:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.successors = []
        self.feature = []

    def add_successor(self, successor):
        """연결된 후속 노드를 추가합니다   ++."""
        self.successors.append(successor)

    def node_to_dot(self):
        viz_code = ""

        if len(self.successors) > 1:
            viz_code += f'{self.id} -> {self.successors[0]} [label = "true" labelStyle = "fill: #77f; font-weight: bold;"];\n'
            viz_code += f'{self.id} -> {self.successors[1]} [label = "false" labelStyle = "fill: #f77; font-weight: bold;"];\n'
        elif len(self.successors) == 1:
            viz_code += f'{self.id} -> {self.successors[0]};\n'

        return viz_code
