from Node import Node


class Queue:
    length = 0
    current = None

    def __init__(self, head=None):
        self.head = Node(head)
        if head:
            self.length += 1

    def __str__(self):
        self.current = self.head
        content = []
        while self.current:
            content.append(self.current.node)
            self.current = self.current.next_node
        self.current = self.head
        return str(content)

    def empty(self):
        if self.length == 0:
            return True
        else:
            return False

    def get_head(self):
        return self.head

    # def set_head(self, new_head):
    #    self.head = new_head

    def get_element(self, index):
        if index <= self.length & index > 0:
            self.current = self.head
            c = 1
            while c < index:
                c += 1
                self.current = self.current.next_node
            return self.current.node
        else:
            return None

    def pop(self):
        self.length -= 1
        el = self.head.node
        self.head = self.head.next_node
        return el

    def push(self, new_head):
        self.length += 1
        old_head = self.head
        self.head = Node(new_head)
        self.head.set_next(old_head)
