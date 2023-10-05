import threading


class RRSem:
    mtx = threading.Semaphore()
    blocked = []                    # list of private semaphores blocked
    running_after_check = {}        # true if thread i didn't complete q and it has other operations to do
    nt = nb = 0
    stop_event = threading.Event()  # event that stops the checking existence of the running_after_check thread
    idt = 0                         # running_after_check thread id that finished his q
    thread_started = False

    def __init__(self, q, multiple_queues=False):
        self.q = q
        self.multiple_queues = multiple_queues
        self.check_th = threading.Thread(target=self.check_ending_thread)

    def check_ending_thread(self):
        find = False
        while not self.stop_event.is_set():
            for i in threading.enumerate():
                if i.native_id == self.idt:
                    find = True
            if find is False:
                self.change_runner()
                del self.running_after_check[self.idt]
                break
            find = False
        self.stop_event.clear()

    def before(self, i=-1):
        s_r = threading.Semaphore(value=0)
        self.mtx.acquire()
        if i not in self.running_after_check:
            self.running_after_check[i] = False
        if ((self.nt > 0) | (self.nb > 0)) & (self.running_after_check[i] is False):
            self.nb += 1
            if i != -1:
                print('thread {} BLOCKED'.format(i))
            self.blocked.append(s_r)
        else:
            self.nt += 1
            s_r.release()
        if self.running_after_check[i] is True:
            self.running_after_check[i] = False
            self.stop_event.set()
        self.mtx.release()
        s_r.acquire()

    def after(self, t, i):
        self.mtx.acquire()
        self.nt -= 1
        ris = False
        if self.change_thread(t):
            self.running_after_check[i] = False
            if not self.multiple_queues:
                self.release_blocked()
            else:
                ris = True
        else:
            self.idt = i
            self.running_after_check[i] = True
            try:
                threading.Thread(target=self.check_ending_thread).start()
            except Exception:
                raise RuntimeError('ERROR starting checking thread')
        self.mtx.release()
        if self.multiple_queues:
            return ris

    def change_runner(self):
        self.mtx.acquire()
        self.release_blocked()
        self.mtx.release()

    def change_thread(self, t):
        if t >= self.q:
            return True
        return False

    def release_blocked(self):
        if self.nb > 0:
            s_r = self.blocked.pop(0)
            self.nb -= 1
            self.nt += 1
            s_r.release()
