from Node import Node
from threading import Semaphore
from Sem import Sem


class FifoQueue:
    s = Sem()
    length = 0
    current = Node()

    def __init__(self, head=None):
        self.head = Node(head)
        if head:
            self.length += 1

    def __str__(self):
        self.current = self.head
        content = []
        if self.length:
            while self.current is not None:
                content.append(self.current.get_node())
                self.current = self.current.get_next()
        self.current = self.head
        return str(content)

    def empty(self):
        if not self.length:
            return True
        else:
            return False

    def get_head(self):
        return self.head

    def get_length(self):
        return self.length

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

    def push(self, new_node):
        if not self.length:
            self.head = Node(new_node)
        else:
            old_head = self.head
            while self.head.get_next() is not None:
                self.head = self.head.get_next()
            self.head.set_next(new_node)
            self.head = old_head
        self.length += 1

