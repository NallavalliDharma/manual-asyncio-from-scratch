### EventLoop
# The main job of the eventloop is Take something that is ready to run from the queue and excute it.
# for storing the tasks we will use from collections import deque
# self.ready = deque() 
# For example we have tasks [A,B,C] it will use FIFO operaion
# So first A excutes now [B,C] when A pauses so it should add again in deque so now [B,C,A] and B excutes it will continue.

## First we test only call_soon() and run_forever()
from .step5_task_test import Task
from collections import deque

class EventLoop:
  def __init__(self):
    self.ready = deque()
### Problem Statement says that call_soon() should put a callback into the ready queue, not to excute immediatley
  def call_soon(self,callback,*args):
    self.ready.append((callback,args))
### so for excuting those we will use below one
  def run_forever(self):
    self.running = True
    while self.running and self.ready:
      callback , args = self.ready.popleft()
      callback(*args)

  def create_task(self,coroutine):
    task = Task(self,coroutine) # So we creating the object(task) for a class (Task) and sending which coroutine should run
    self.call_soon(task.step) #here first understand what task.step will do -> in Task class step will start/resume the coroutine -> yieled  and using exception we will get value and  notic we did not keep task.step() we just wrote task.step because we dont want implement now so we want to tell event loop to excute it.
    # So call_soon puts this into ready queue and then run_forever takes it.
    return task

  def stop(self): # with this we can stop the loop whenever we cant. without this we cant stop untill readyqueue becomes empty.
    self.running = False

  def run_untill_complete(self,task): #Run the EventLoop until this specific Task is finished.
    self.running = True
    while self.running and not task.done():
      if self.ready:
        callback , args = self.ready.popleft()
        callback(*args)
    






loop = EventLoop()
loop.call_soon(print,"Hello") # this adds the [("hello")]
loop.call_soon(print,"World") # here [("hello"),("World")]
print("Before Loop")
loop.run_forever()  # so for first iteration callback -> print and argument is "Hello" so print("Hello") and same for next "World"
print("After Loop")
