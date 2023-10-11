# RTES_Project

An implementation of a thread-safe queue.  
It is possibile to access the queue with different methods and you can use 4 different types of scheduling policies: Fifo, Priority, Round-Robin and Multiple Queues.  
The result is avavilable as a list, using the print method.

## Queue
When you choose a policy and create an istance of it, automatically the queue is created and you can insert the first element as a parameter (Head).
>
There are 5 methods to access the queue:
>
  *push*: insert a new node at the end of the queue. (writing)  
  >
  *pop*: removes the head of the queue, and returns that element. (writing)
  >
  *get_length*: returns the number of elements inside the queue. (read-only)  
  >
  *empty*: True if it's empty, False otherwise. (read-only)
  >
  *get_head*: returns the first element, without dropping it. (read-only)  

## Scheduling policies
The parallel acccess of multiple threads to the queue are managed in 4 possible ways:
>
*Fifo*: the first thread arrived is the first to be served. You can invoke the object **FifoPolicy** and use the methods above.
>
*Priority*: the first thread to be served is the one with the highest priority. You can invoke the object **PrioPolicy** and use the methods above, specifying the priority every time. 
>
*Round Robin*: during the invocation of the **RRPolicy** object insert the q parameter to indicate how many seconds a thread can be served. If q is not enough the thread return at the back of the waiting queue.
>
*Multiple Queues*: the object **MQPolicy** accepts a list of q as a parameter and for every q it creates
a RRPolicy instance and it adds a FifoPolicy at the end. Every thread starts from the queue with the smallest q and if it doesn't complete his tasks it will be assigned to the lower queues.
 >
If you want to see some examples check the directory example
