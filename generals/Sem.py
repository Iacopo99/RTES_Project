from threading import Semaphore


class Sem:
    __mtx = Semaphore()
    __private_w = {}
    __private_r = {}
    __nw = __nbw = __nr = __nbr = 0

    def before_reading(self):
        pass

    def after_reading(self):
        pass

    def before_writing(self):
        pass

    def after_writing(self):
        pass
