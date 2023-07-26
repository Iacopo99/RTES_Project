from threading import Semaphore
from generals.ImplementSem import ImplementSem


class FifoSem(ImplementSem):

    def before_writing(self, i=-1):
        s_w = Semaphore(value=0)
        self.__mtx.acquire()
        if (self.__nr > 0) | (self.__nw > 0):
            self.__nbw += 1
            c = self.__nbw
            if i != -1:
                print('thread writer {} BLOCKED'.format(i))
            self.private_w[c] = s_w
        else:
            self.__nw += 1
            s_w.release()
        self.__mtx.release()
        s_w.acquire()

    def after_writing(self):
        self.__mtx.acquire()
        self.__nw -= 1
        if self.__nbr > 0:
            while self.__nbr > 0:
                self.__nbr -= 1
                self.__nr += 1
                s_r = self.private_r.pop(1)
                s_r.release()
                new = {}
                for i in self.private_r.keys():
                    new[i - 1] = self.private_r[i]
                self.private_r = new
        elif self.__nbw > 0:
            self.__free_writer()
        self.__mtx.release()

    def __free_writer(self):
        self.__nbw -= 1
        self.__nw += 1
        s_w = self.__private_w.pop(1)
        s_w.release()
        new = {}
        for i in self.__private_w.keys():
            new[i - 1] = self.__private_w[i]
        self.private_w = new
