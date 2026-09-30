### __await__
# def __await__(self):
#   if not self._done:
#     yield self
#   return self._result

### Understanding __await__ :
# future = Future() then __init__ constructor does self._done = False and seld._result = None 
# so if not self._done becomes if not False means if True excute yield self(Pause this i doesn't have any result let another task run and comeback when result available)
#So who makes self._done will make True => Future.set_result() makes self._done True 
# so now if not self._done becomes if not True means if False so doesn't excute directly now result will be returned

### Entire Future becomes
class Future:

    def __init__(self):
        self._done = False
        self._result = None
        self._callbacks = []

    def done(self):
        return self._done

    def result(self):
        if not self._done:
            raise Exception("Future is not done")

        return self._result

    def set_result(self, value):
        if self._done:
            raise Exception("Future is already done")

        self._result = value
        self._done = True

        for callback in self._callbacks: # when coroutine excutes we will register and when the task get finished then we will call back using from this 
            callback(self)

    def add_done_callback(self, callback):
        self._callbacks.append(callback)

    def __await__(self):
        if not self._done:
            yield self

        return self._result
###So the return self._result doesn't execute while the Future is still pending. It executes after the Future has been completed and the coroutine has been resumed.
