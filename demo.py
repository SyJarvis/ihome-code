import functools


def login_required(func):
    @functools.wraps(func)
    def wrapper(*arg, **kwargs):
        pass

    return wrapper

@login_required
def itcast():
    """itcast python"""
    pass

# itcast--->wrapper
print(itcast.__name__)
print(itcast.__doc__)