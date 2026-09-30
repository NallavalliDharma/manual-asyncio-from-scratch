class Future:
  def __init__(self):
    self._done = False
    self._result = None
    self._callbacks = []

  def done(self):
    return self._done

  def result(self):
    if not self._done:
      raise Exception("Future is not done ")
    return self._result

  def set_result(self,value):
    if self._done:
      raise Exception("Future is already done")
    self._result = value
    self._done = True

    for callback in self._callbacks:
      callback(self)

  def add_done_callback(self,callback):
    if self._done:
      callback(self)
    else:
      self._callbacks.append(callback)

  def __await__(self):
    if not self._done:
      yield self

    return self._result



  