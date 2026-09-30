class YieldControl:
  def __await__(self):
    yield self

def yield_control():
  return YieldControl()