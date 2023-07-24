from threading import Semaphore
from Generals.ImplementSem import ImplementSem


class FifoSem(ImplementSem):

    def before_writing(self, i=-1):
        s_w = Semaphore(value=0)
        self.mtx.acquire()
        if (self.nr > 0) | (self.nw > 0):
            self.nbw += 1
            c = self.nbw
            if i != -1:
                print('thread writer {} BLOCKED'.format(i))
            self.private_w[c] = s_w
        else:
            self.nw += 1
            s_w.release()
        self.mtx.release()
        s_w.acquire()

    def after_writing(self):
        self.mtx.acquire()
        self.nw -= 1
        if self.nbr > 0:
            while self.nbr > 0:
                self.nbr -= 1
                self.nr += 1
                s_r = self.private_r.pop(1)
                s_r.release()
                new = {}
                for i in self.private_r.keys():
                    new[i - 1] = self.private_r[i]
                self.private_r = new
        elif self.nbw > 0:
            self.free_writer()
        self.mtx.release()

    def free_writer(self):
        self.nbw -= 1
        self.nw += 1
        s_w = self.private_w.pop(1)
        s_w.release()
        new = {}
        for i in self.private_w.keys():
            new[i - 1] = self.private_w[i]
        self.private_w = new
