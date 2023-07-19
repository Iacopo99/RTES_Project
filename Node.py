class Node:
    next_node = None

    def __init__(self, node=None):
        self.node = node

    def __str__(self):
        return str(self.node)

    def get_node(self):
        return self.node

    def set_node(self, node):
        self.node = node

    def get_next(self):
        return self.next_node

    def set_next(self, next_node):
        self.next_node = Node(next_node)
