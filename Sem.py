from threading import Semaphore


class Sem:
    mtx = Semaphore()
    private_w = Semaphore(value=0)
    private_r = Semaphore(value=0)
    nw = nbw = nr = nbr = 0

    def before_reading(self, i):
        self.mtx.acquire()
        if self.nw > 0 | self.nbw > 0:
            self.nbr += 1
            print('thread reader {} blocked'.format(i))
        else:
            self.nr += 1
            self.private_r.release()
        self.mtx.release()

    def after_reading(self):
        self.mtx.acquire()
        self.nr -= 1
        if self.nbw > 0 & self.nr == 0:
            self.nbw -= 1
            self.nw += 1
            self.private_w.release()
        self.mtx.release()

    def before_writing(self, i):
        self.mtx.acquire()
        if self.nr > 0 | self.nw > 0:
            self.nbw += 1
            print('thread writer {} blocked'.format(i))
        else:
            self.nw += 1
            self.private_w.release()
        self.mtx.release()

    def after_writing(self):
        self.mtx.acquire()
        if self.nbr > 0:
            while self.nbr > 0:
                self.nbr -= 1
                self.nr += 1
                self.private_r.release()
        elif self.nbw > 0:
            self.nbw -= 1
            self.nw += 1
            self.private_w.release()
        self.mtx.release()
