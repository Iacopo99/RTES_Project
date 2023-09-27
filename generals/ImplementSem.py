from threading import Semaphore
from generals.Sem import Sem


class ImplementSem(Sem):

    def before_reading(self, i=-1):
        s_r = Semaphore(value=0)
        self.mtx.acquire()
        if (self.nw > 0) | (self.nbw > 0):
            self.nbr += 1
            c = self.nbr
            if i != -1:
                print('thread reader {} BLOCKED'.format(i))
            self.private_r[c] = s_r
        else:
            self.nr += 1
            s_r.release()
        self.mtx.release()
        s_r.acquire()

    def after_reading(self):
        self.mtx.acquire()
        self.nr -= 1
        if (self.nbw > 0) & (self.nr == 0):
            self.free_writer()
        self.mtx.release()

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
        pass
