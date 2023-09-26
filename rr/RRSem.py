import threading


class RRSem:
    mtx = threading.Semaphore()
    __blocked = []
    running = {}
    nt = nb = 0
    stop_event = threading.Event()
    # c = 0
    check_th = 0
    idt = 0
    thread_started = False

    def __init__(self, q):
        self.q = q
        self.check_th = threading.Thread(target=self.main_t)

    def main_t(self):
        find = False
        while not self.stop_event.is_set():
            for i in threading.enumerate():
                if i.native_id == self.idt:
                    find = True
            if find is False:
                self.change_runner()
                break
            find = False
        self.stop_event.clear()

    def before(self, i=-1):
        s_r = threading.Semaphore(value=0)
        self.mtx.acquire()
        if i not in self.running:
            self.running[i] = False
        if ((self.nt > 0) | (self.nb > 0)) & (self.running[i] is False):
            self.nb += 1
            if i != -1:
                print('thread {} BLOCKED'.format(i))
            self.__blocked.append(s_r)
        else:
            self.nt += 1
            s_r.release()
        if self.running[i] is True:
            self.stop_event.set()
        self.mtx.release()
        s_r.acquire()

    def after(self, t, i):
        self.mtx.acquire()
        self.nt -= 1
        if self.change_thread(t):
            self.running[i] = False
            if self.nb > 0:
                s_r = self.__blocked.pop(0)
                self.nb -= 1
                self.nt += 1
                s_r.release()
        else:
            self.idt = i
            self.running[i] = True
            try:
                self.check_th.start()
                self.check_th = threading.Thread(target=self.main_t)
            except Exception:
                raise RuntimeError('ERROR starting checking thread')
        self.mtx.release()

    def change_runner(self):
        self.mtx.acquire()
        if self.nb > 0:
            s_r = self.__blocked.pop(0)
            self.nb -= 1
            self.nt += 1
            s_r.release()
        self.mtx.release()

    def change_thread(self, t):
        if t >= (self.q * 0.85):
            return True
        return False
