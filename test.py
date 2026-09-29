### Step1:coroutine.send(None)
async def hello():
  print("Hello")
  return 24
coro = hello()
# coro.send(None) -> "Start/resume this coroutine and let it execute until it either finishes or reaches an await point."
#there is an important thing here. coroutine does not return 24 value normally from send, Python raises stopIteration and the return value store inside the exception : exception.value this is what exactly described in problem statement.

try:
  result = coro.send(None)
  print("yielded: ",result)

except StopIteration as e:
  print("Coroutine completed")
  print("Result: ",e.value)

### Understanding :
# coro = hello() -> coroutine object created.
# coro.send(None) -> hello() starts executing.
# and then Hello printed.
# In StopIteration exception returned value will be stored
# e.value - 24
# ============================================================

### Step2 : await
# The problem says that Task must pause when a coroutine awaits an incomplete Future and later resume when the Future completes.
# What is await : await is a mechanism that suspending the current coroutine and allowing whoever driving that coroutine to regain control which is exactly want 
# result = await future => meaning of this line : "I need the result of this awaitable , if isn't ready suspend me and resume when it becomes ready."
class Something:
  def __await__(self):
    yield "PAUSED"

async def worker():
  print("A")

  await Something()

  print("B")

corout = worker()

try:
  value = corout.send(None)
  print("Coroutine yielded: ",value)

except StopIteration as e:
  print("Finished ",e.value)
### Understanding:
# so here only A print and then the StopIteration contain the value is PAUSED so it prints. Noticed that B did not print because await Something() Paused we need to resume that so everytime we can not do corout.send(...) so thats why we should use yield_control() 
# yield_control() --> I want to pause here, let another Task run, and then schedule me again.
# By using the function yield_control() -> Task starts and corout.send(None) excutes and prints A and then yield_control comes into the picture and pauses the task and task push back into ready_queue  and then another task run and later first task resume so here B prints.
# ===========================================================




