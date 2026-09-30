# the main job of yield_control is : it should pause the current Task and put that Task at the back of the ready queue.
# so if the queue is [A,B] anad A runs then A yields.now queue is [B,A] yielded A comes back to queue and run later and then B runs.
# why can't we use  "yield self " : -> There is no Future that needs to become complete.  The assignment specifically describes yield_control() as an awaitable that causes the current Task to be scheduled again at the end of the ready queue.
# async def yield_control():
#     yield    -> this is  not correct : Because an async def containing yield becomes an async generator, not a normal coroutine.
class YieldControl:
  def __await__(self):
    yield self

def yield_control():
  return YieldControl() #will eventually yield the YieldControl object to our Task.

  
