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
            viz_code += f'{self.id} -> {self.successors[0]} [label = "true", fontcolor="blue"];\n'
            viz_code += f'{self.id} -> {self.successors[1]} [label = "false", fontcolor="red"];\n'
        elif len(self.successors) == 1:
            viz_code += f'{self.id} -> {self.successors[0]};\n'

        return viz_code
