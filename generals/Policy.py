from generals.ImplementSem import ImplementSem
import random
import time
from generals.NormalQueue import NormalQueue


class Policy:
    s = ImplementSem()

    def __init__(self, head=None):
        """
        Create an FifoQueue object
        :param head: If specified insert the first element of the queue. Otherwise the queue created is empty.
        """
        self.nq = NormalQueue(head)

    def __str__(self):
        self.s.before_reading()
        ris = self.nq.str_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def empty(self):
        """
        Returns a boolean variable. True if the queue is empty (no elements), False otherwise
        :return: Boolean variable
        """
        self.s.before_reading()
        ris = self.nq.empty_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def get_head(self):
        """
        Returns the first object in the queue
        :return: Any possible type of object
        """
        self.s.before_reading()
        ris = self.nq.get_head_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def get_length(self):
        """
        Returns the number of elements in the queue
        :return: An integer the represent the length
        """
        self.s.before_reading()
        ris = self.nq.get_length_not_safe()
        time.sleep(float(random.randint(0, 300) / 1000))
        self.s.after_reading()
        return ris

    def pop(self):
        """
        Select the first item in the queue and deletes the object from it
        :return: The first object of the queue
        """
        self.s.before_writing()
        ris = self.nq.pop_not_safe()
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.s.after_writing()
        return ris

    def push(self, new_node):
        """
        Add an item at the end of the fifo Queue
        :param new_node: It is the item to add in the queue
        :return: Nothing
        """
        self.s.before_writing()
        self.nq.push_not_safe(new_node)
        time.sleep(float(random.randint(0, 1000) / 1000))
        self.s.after_writing()
