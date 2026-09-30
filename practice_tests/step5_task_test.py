### Implementing Task 

# The assignment explicitly requires Task to inherit from Future
# reason : task mainly do 2things
 ## 1) task runs a coroutine
 ## 2) eventually contains the coroutine's result (means future result ) so task should inerit future 

## What should a Task store?
# The problem statement says that  a Task owns one coroutine.and specifically suggest self.coroutine =  coroutine

##SO our intial task can be:
from practice_tests.yield_control_test import YieldControl
from practice_tests.step4_future_test import Future
from practice_tests.step6_eventloop_test import EventLoop
class Task(Future):
  def __init__(self,coroutine,loop): 
    super().__init__() #This calls Future.__init__()
    self.coroutine = coroutine
    self.loop = loop  #Because later, when the Task needs to become runnable again, it needs to tell the EventLoop: ->"Put me back into the ready queue."
## The main job of task is manually advance the coroutine means  use coroutine.send(value) to start/resume the coroutine.so for that we will create the method call step()
  def step(self,value=None): #Means Run this Task's coroutine until it either pauses or finishes.
    try:
      yielded = self.coroutine.send(value)
    except StopIteration as e:
      self.set_result(e.value)
      return
### register task
# when future incompletes (await future) yield future excutes means it pauses so that task registers callbacks and it should pause 
    if isinstance(yielded,Future):
      yielded.add_done_callback(self._wakeup)
    elif isinstance(yielded,YieldControl):
      self.loop.call_soon(self.step)
### Why isinstance function -> yielded means self.coroutine.send(None) so when it excutes the coroutine and reaches to await future there Future.__await__ function will check if task paused or not if paused it excutes yield so yielded gets future. so therefore yielded is the Future object that the coroutine is waiting for.

## isinstance() mean? -> isinstance(yielded, Future) asks "Is the object stored in yielded a Future?" so isinstance(future, Future) is True so "If the coroutine is waiting for a Future, do something about that Future."

## Why do we check that -> Task should know what it yielded
#  ↓
# coroutine.send(None)
#  ↓
# await future
#  ↓
# yielded = future

### yielded.add_done_callback(...) this line tells : ->"Future, remember this callback and run it when you become DONE."

  def _wakeup(self,future):
    self.loop.call_soon(self.step, future.result())
    # So when task get finished -> when we send the value 
    # so future.set_result(100) using this we send the value
    # so future.result() -> 100
    # therefore self.loop.call_soon(self.step, future.result())
    # so in call_soon function self.loop.call_soon(self.step, 100) puts:(self.step, (100,))into the ready queue.
    # The Task is now ready to resume.
    # so run_forever(eventLoop) picks up and excutes and task get completed.











### why this _wakeup when the future finishes and got the result so this stored callback called using that.

# Flow for understanding
# Task runs
#    ↓
# coroutine.send(None)
#    ↓
# await future
#    ↓
# Future.__await__()
#    ↓
# yield future
#    ↓
# yielded = future
#    ↓
# isinstance(yielded, Future)
#    ↓
# True
#    ↓
# yielded.add_done_callback(self._wakeup)
#    ↓
# Task pauses
#    ↓
# future.set_result(100)
#    ↓
# Future becomes DONE
#    ↓
# Future calls _wakeup()
#    ↓
# Task can be resumed





# testing:
async def calculate():
    return 42


task = Task(calculate())

task.step()

print(task.done())
print(task.result())
