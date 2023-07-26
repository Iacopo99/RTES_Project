from generals.Node import Node


class NormalQueue:
    __length = 0
    __current = Node()

    def __init__(self, head=None):
        self.__head = Node(head)
        if head:
            self.__length += 1

    def str_not_safe(self):
        self.__current = self.__head
        content = []
        if self.__length:
            while self.__current is not None:
                content.append(self.__current.get_node())
                self.__current = self.__current.get_next()
        self.__current = self.__head
        return str(content)

    def empty_not_safe(self):
        if not self.__length:
            return True
        else:
            return False

    def get_head_not_safe(self):
        return self.__head

    def get_length_not_safe(self):
        return self.__length

    def pop_not_safe(self):
        if self.__length:
            self.__length -= 1
            el = self.__head.node
            self.__head = self.__head.next_node
            return el
        else:
            return None

    def push_not_safe(self, new_node):
        if not self.__length:
            self.__head = Node(new_node)
        else:
            old_head = self.__head
            while self.__head.get_next() is not None:
                self.__head = self.__head.get_next()
            self.__head.set_next(new_node)
            self.__head = old_head
        self.__length += 1
