# decorator for coroutine
def coroutine(func):
    def wrap(*args, **kwargs):
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap
