from collections import deque
from Tasks import Task

class EventLoop:
  def __init__(self):
    self.ready = deque()
    self.running = False

  def call_soon(self,callback,*args):
    self.ready.append((callback,args))

  def create_task(self,coroutine):
    task = Task(self,coroutine)
    self.call_soon(task.step)
    return task

  def run_forever(self):
    self.running = True

    while self.running and self.ready:
      callback,args = self.ready.popleft()
      callback(*args)
      

  def run_until_complete(self,task):
    self.running = True

    while self.running and not task.done():

      if self.ready:
        callback,args = self.ready.popleft()
        callback(*args)
      else:
        break
    return task.result()

  def stop(self):
    self.running = False
    


