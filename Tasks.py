from future import Future
from yield_control import YieldControl

class Task(Future):
  def __init__(self,loop,coroutine):
    super().__init__()

    self.loop = loop
    self.coroutine = coroutine


  def step(self,value=None):
    try:
      yielded = self.coroutine.send(value)
    except StopIteration as e:
      self.set_result(e.value)
      return
#    Wait until that Future finishes.
    if isinstance(yielded,Future):
      yielded.add_done_callback(self._wakeup)
#   I voluntarily yielded; schedule me again.
    elif isinstance(yielded,YieldControl):
      self.loop.call_soon(self.step)

#    Future finished, so schedule this Task again with the Future's result.
  def _wakeup(self,future):
    self.loop.call_soon(self.step,future.result())