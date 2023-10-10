import threading


class MQSem:
    num_queue = {}  # queue associated to each thread
    mtx = threading.Semaphore()
    nt = 0
    nb = []  # number of blocked threads on every queue
    thread_sem = {}  # semaphore for each thread
    block_on_queue = {}  # list of id threads blocked on every queue
    already_released = False  # check if the thread already released another thread
    change_t = False
    stop_event = threading.Event()  # event that stops the thread
    idt = 0
    running_after_check = {}    # true if thread i didn't complete q and it has other operations to do
    active = False  # True if a thread is executing

    def __init__(self, queue_list):
        self.queue_list = queue_list
        self.num_q = len(self.queue_list)  # number of queue created
        for c in range(self.num_q):
            self.nb.append(0)
            self.block_on_queue[c] = []

    def before(self, i, read=False):
        block = False
        first_pass = False
        self.mtx.acquire()
        if i not in self.thread_sem:
            self.thread_sem[i] = threading.Semaphore(value=0)
            first_pass = True
        if i not in self.running_after_check:
            self.running_after_check[i] = False
        if self.change_t | first_pass:
            for c in range(self.num_queue[i]):
                if ((self.nb[c]) | self.queue_list[c].sem.nb | self.queue_list[c].sem.nt) & (self.running_after_check[i] is False):
                    block = True
                    break
            if self.num_queue[i] == (self.num_q - 1):
                if read:
                    if (self.nb[self.num_queue[i]]) | self.queue_list[self.num_queue[i]].sem.nbw | self.queue_list[self.num_queue[i]].sem.nw:
                        block = True
                else:
                    if (self.nb[self.num_queue[i]]) | self.queue_list[self.num_queue[i]].sem.nr | self.queue_list[self.num_queue[i]].sem.nw:
                        block = True
            if self.active & (self.running_after_check[i] is False) & (self.num_queue[i] < (self.num_q - 1)):
                block = True
            if block:
                self.nb[self.num_queue[i]] += 1
                self.block_on_queue[self.num_queue[i]].append(i)
                print('thread {} BLOCKED on the queue {}'.format(i, self.num_queue[i]))
            self.change_t = False
        if self.running_after_check[i]:
            self.running_after_check[i] = False
            self.stop_event.set()
        if not block:
            self.thread_sem[i].release()
            self.active = True
        self.mtx.release()
        self.thread_sem[i].acquire()

    def change_queue(self, i, t):
        if self.num_queue[i] < (self.num_q - 1):
            if self.queue_list[self.num_queue[i]].sem.after(t, i):
                self.num_queue[i] += 1
                print('assigning thread {} to the queue {}'.format(i, self.num_queue[i]))
                return True
        return False

    def check_ending_thread(self):
        find = False
        if self.num_queue[self.idt] < (self.num_q - 1):
            while not self.stop_event.is_set():
                for i in threading.enumerate():
                    if i.native_id == self.idt:
                        find = True
                if find is False:
                    self.safe_release(self.idt)
                    del self.running_after_check[self.idt]
                    break
                find = False
        self.stop_event.clear()

    def realising_higher_queues(self, i):
        for c in range(self.num_queue[i]):
            if self.nb[c]:
                ris = self.block_on_queue[c].pop(0)
                self.thread_sem[ris].release()
                self.nb[c] -= 1
                self.already_released = True
                break
            elif self.queue_list[c].sem.nb:
                self.queue_list[c].sem.change_runner()
                self.already_released = True
                break
        return self.already_released

    def realising_current_queue(self, i, ch=False, read=False):
        if self.nb[self.num_queue[i]]:
            ris = self.block_on_queue[self.num_queue[i]].pop(0)
            self.thread_sem[ris].release()
            self.nb[self.num_queue[i]] -= 1
            self.already_released = True
        elif self.num_queue[i] < (self.num_q - 1):
            if self.queue_list[self.num_queue[i]].sem.nb:
                self.queue_list[self.num_queue[i]].sem.change_runner()
                self.already_released = True

        if read & (self.num_queue[i] == (self.num_q - 1)) & (not ch):
            self.queue_list[self.num_queue[i]].sem.after_reading()
            self.already_released = True
        elif (self.num_queue[i] == (self.num_q - 1)) & (not ch):
            self.queue_list[self.num_queue[i]].sem.after_writing()
            self.already_released = True
        return self.already_released

    def realising_lower_queues(self, i):
        for c in range(self.num_queue[i] + 1, self.num_q):
            if c < (self.num_q - 1):
                self.queue_list[c].sem.change_runner()
                break
            elif (not self.queue_list[c].sem.nr) & self.queue_list[c].sem.nbw:
                self.queue_list[c].sem.after_reading()
            elif self.queue_list[c].sem.nbr:
                self.queue_list[c].sem.after_writing()

    def safe_release(self, i):
        self.mtx.acquire()
        self.thread_release(i)
        self.mtx.release()

    def thread_release(self, i, ch=False, read=False):
        self.change_t = True
        if not self.realising_higher_queues(i):
            if not self.realising_current_queue(i, ch, read):
                self.realising_lower_queues(i)
        if self.already_released:
            self.already_released = False
            self.active = True
        else:
            self.active = False

    def after(self, i, t=-1, read=False):
        self.mtx.acquire()
        if self.num_queue[i] < (self.num_q - 1):
            if self.change_queue(i, t):
                self.thread_release(i, True)
            else:
                self.idt = i
                self.running_after_check[i] = True
                try:
                    threading.Thread(target=self.check_ending_thread).start()
                except Exception:
                    raise RuntimeError('ERROR starting checking thread')
        else:
            self.thread_release(i, read=read)
        self.mtx.release()
