from threading import Semaphore
from generals.Sem import Sem


class ImplementSem(Sem):

    def before_reading(self, i=-1):
        s_r = Semaphore(value=0)
        self.__mtx.acquire()
        if (self.__nw > 0) | (self.__nbw > 0):
            self.__nbr += 1
            c = self.__nbr
            if i != -1:
                print('thread reader {} BLOCKED'.format(i))
            self.__private_r[c] = s_r
        else:
            self.__nr += 1
            s_r.release()
        self.__mtx.release()
        s_r.acquire()

    def after_reading(self):
        self.__mtx.acquire()
        self.__nr -= 1
        if (self.__nbw > 0) & (self.__nr == 0):
            self.__free_writer()
        self.__mtx.release()

    def __free_writer(self):
        pass
