class Future:
  def __init__(self):
    self._done = False
    self._result = None
    self._callbacks = []

### for implementing future.done()
  def done(self):
    return self._done
### for implementing future.set_result()
  def set_result(self,value):
    if self._done:
      raise Exception("Future is already done")   
    self._result = value
    self._done = True
    return self._result
### implementinf future.()
  def result(self):
    if not self._done:
      raise Exception("Future is not done")
    return self._result

### the important part : add_done_callback()
# this is where future class usefull for task/eventloop
# Why? : Suppose a task is waiting for a Future: The task needs to somehow says When this Future finishes, wake me up. thats what the callback is for.
# Future becomes Done and then callback excutes and task becomes runnable.


future = Future()
print("Done: ",future.done())
try:
  print(future.result())
except Exception as e:
  print("Error: ",e)
future.set_result(12)
print("Done: ",future.done())
print("Result:", future.result())

