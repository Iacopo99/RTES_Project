from fifo.FifoPolicy import FifoPolicy
from rr.RRPolicy import RRPolicy
from generals.Policy import Policy
from multiple_queues.MQSem import MQSem
import time
import random


class MQPolicy(Policy):
    queue_list = []

    def __init__(self, list_q, head=None):
        super().__init__(head)
        exc = False
        if type(list_q) is not list:
            exc = True
        for i in list_q:
            if type(i) is not int and type(i) is not float:
                exc = True
        if exc:
            raise ValueError('parameter list_q must be a list of int')
        for q in sorted(set(list_q)):
            self.queue_list.append(RRPolicy(q=q, multiple_queues=True))
            print('Queue created: q = {}'.format(q))
        self.queue_list.append(FifoPolicy())
        print('Fifo Queue created')
        self.sem = MQSem(self.queue_list)

    def general_reader(self, func, i):
        if i not in self.sem.num_queue:
            self.sem.num_queue[i] = 0
        self.sem.before(i)
        if self.sem.num_queue[i] != (len(self.queue_list) - 1):
            self.queue_list[self.sem.num_queue[i]].sem.before(i)
        else:
            self.queue_list[self.sem.num_queue[i]].sem.before_reading(i)
        start = time.time()
        ris = func()
        time.sleep(float(random.randint(0, 300) / 1000))
        end = time.time()
        if self.sem.num_queue[i] != (len(self.queue_list) - 1):
            t = self.queue_list[self.sem.num_queue[i]].calculate_t(i, end - start)
            print('{} seconds to execute the operation by the thread {}'.format(t, i))
        else:
            t = 0
        if self.sem.num_queue[i] != (len(self.queue_list) - 1):
            self.sem.after(i, t)
        else:
            self.sem.after(i, t, True)
        return ris

    def empty(self, i):
        return self.general_reader(self.nq.empty_not_safe, i)

    def get_head(self, i):
        return self.general_reader(self.nq.get_head_not_safe, i)

    def get_length(self, i):
        return self.general_reader(self.nq.get_length_not_safe, i)

    def general_writer(self, func, i, node=None):
        if i not in self.sem.num_queue:
            self.sem.num_queue[i] = 0
        self.sem.before(i)
        if self.sem.num_queue[i] != (len(self.queue_list) - 1):
            self.queue_list[self.sem.num_queue[i]].sem.before(i)
        else:
            self.queue_list[self.sem.num_queue[i]].sem.before_writing(i)
        start = time.time()
        if node is None:
            ris = func()
        else:
            ris = func(node)
        time.sleep(float(random.randint(0, 300) / 1000))
        end = time.time()
        if self.sem.num_queue[i] != (len(self.queue_list) - 1):
            t = self.queue_list[self.sem.num_queue[i]].calculate_t(i, end - start)
            print('{} seconds to execute the operation by the thread {}'.format(t, i))
        else:
            t = 0
        self.sem.after(i, t)
        return ris

    def pop(self, i):
        return self.general_writer(self.nq.pop_not_safe, i)

    def push(self, i, new_node):
        self.general_writer(self.nq.push_not_safe, i, new_node)
