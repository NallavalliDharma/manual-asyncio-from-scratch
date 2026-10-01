This project was implemented manually, step by step, without using Python's built-in `asyncio` or other restricted concurrency modules.

The step-by-step implementation and individual testing performed during development are available in the practice_tests folder.

Each concept was implemented and tested individually before moving to the next step.
============================================================

1. What is a coroutine?

A coroutine is a function defined using async ddef.
this async function does not immediately excute its body. It creates a coroutine object that can be excuted and resumed by the event loop.
Example :
async def hello():  ##here async def hello() is coroutine
  return 42

====================================================================================================

2. What is the difference between a coroutine and a Task?
A coroutine is the actual asynchronous computation.
A Task is an object that manages and schedules a coroutine for execution.
For example:
coroutine = hello()
task = loop.create_task(coroutine)

The coroutine contains the work, while the Task is responsible for driving the coroutine using send() and coordinating with the EventLoop.

====================================================================================================

3. What does a Future represent?

A Future represents a value that will become available later.
Initially: 
_done = False
_result = None

after the result provided:
_done = True
_result = Value

A Future can also store callbacks that should be executed when the Future completes.

====================================================================================================

4. Why can a Task inherit from Future?

A Task represents the eventual result of a coroutine.

Therefore, a Task needs many of the same properties as a Future:
-> it has a result
-> it can be pending/complete
-> other coroutines can wait for it
-> it can notify callbacks when it completes

====================================================================================================

5. What happens when a Task starts executing a coroutine?

The Task calls:
coroutine.send(value)
to start or resume the coroutine.

For the first execution, the Task uses:
coroutine.send(None)
The coroutine runs until one of these happens:
-> it returns a result
-> it yields a Future because it is waiting
->It yields the YieldControl object because it voluntarily gives control back to the EventLoop.

If the coroutine returns, Python raises StopIteration internally with the returned value. The Task catches it and stores the value using: self.set_result(e.value)

====================================================================================================

6. What does coroutine.send(None) do?

coroutine.send(None)
starts the coroutine for the first time.

It sends None into the coroutine and allows it to execute until it reaches a yield, await, or returns.

====================================================================================================

7. What happens internally when a coroutine executes await future and the Future is not complete?

Suppose:
result = await future
and:
future._done == False
The Future's __await__() executes:
def __await__(self):
    if not self._done:
        yield self
    return self._result

So the Future object itself is yielded.

The Task receives that Future:
yielded = self.coroutine.send(value)
Then the Task registers its wake-up callback:
yielded.add_done_callback(self._wakeup)

The Task is now suspended until the Future completes.

====================================================================================================

8. How does completing a Future cause a suspended Task to resume?

When the Future completes:
future.set_result(value)

it does:
self._done = True
self._result = value

Then it executes all registered callbacks:
for callback in self._callbacks:
    callback(self)

The Task's _wakeup() method is one of those callbacks.

It schedules the Task again:
def _wakeup(self, future):
    self.loop.call_soon(
        self.step,
        future.result()
    )

So the flow is:

Future completes
      ↓
callback is called
      ↓
Task._wakeup()
      ↓
Task is added to ready queue
      ↓
EventLoop runs Task
      ↓
Task resumes with Future's result

====================================================================================================

9. How does await task work if Task inherits from Future?

Because:
class Task(Future):
a Task inherits the Future's __await__() method.
Therefore:
result = await task

works in the same way as:
result = await future

If the Task is not complete:
if not self._done:
    yield self

The waiting Task registers a callback on the awaited Task.

When the awaited Task finishes, its result is passed back to the waiting Task.

So:
Task A
  |
  | await Task B
  ↓
Task A pauses
  |
  ↓
Task B completes with 100
  |
  ↓
Task A wakes up
  |
  ↓
result = 100

====================================================================================================

10. Why is this scheduling model cooperative rather than preemptive?

It is cooperative because a coroutine controls when it gives control back to the EventLoop.

For example:
await yield_control()

explicitly gives the EventLoop an opportunity to run another Task.

The EventLoop does not interrupt a running coroutine in the middle of its normal Python execution.

The coroutine must reach an await or another yield point for another Task to get a chance to run.

====================================================================================================

11. What happens if one coroutine performs a long-running computation without ever awaiting anything?

That coroutine keeps control of the EventLoop.
For example:
async def bad_worker():
    for i in range(1000000000):
        # long computation
        pass

If it never reaches an await or yields control, the EventLoop cannot switch to another Task.

The other Tasks remain waiting in the ready queue until the long-running coroutine finishes.

Therefore, cooperative scheduling requires coroutines to periodically give control back to the EventLoop.

For example:
async def worker():
    # do some work
    await yield_control()
    # continue working

This allows other ready Tasks to execute.