from FifoSem import FifoSem
from Policy import Policy


class FifoPolicy(Policy):
    s = FifoSem()
