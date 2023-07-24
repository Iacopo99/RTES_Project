from threading import Semaphore


class Sem:
    mtx = Semaphore()
    private_w = {}
    private_r = {}
    nw = nbw = nr = nbr = 0

    def before_reading(self):
        pass

    def after_reading(self):
        pass

    def before_writing(self):
        pass

    def after_writing(self):
        pass
