def list_get (_list, i, default=None):
  try:
    return _list[i]
  except IndexError:
    return default
