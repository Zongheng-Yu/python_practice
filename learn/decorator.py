"""Decorator with parameters must return a decorator.
The most inner decorator usually takes only one parameter which is the function it decorates.

1. decorator(fun)
@decorator
def fun():
    pass

2. decorator_factory(param)(fun)
@decorator_factory(param)
def fun():
    pass

3. decorator_factory(param)(decorator)(fun)
@decorator_factory(param)
@decorator
def fun():
    pass

"""


import time
from functools import partial, wraps


def print_function_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print func.__name__
        return func(*args, **kwargs)

    print wrapper.__name__
    return wrapper


def sample_time_print_decorator(func):
    def wrapper(*args, **kwargs):
        print  time.localtime()
        return func(*args, **kwargs)

    return wrapper


def add_hello_time_print_decorator(func):
    def wrapper(*args, **kwargs):
        print  "hello: ", time.localtime()
        return func(*args, **kwargs)

    return wrapper


def add_anything_time_print_decorator_factory(additional=None):
    def print_time_decorator(func):
        def wrapper(*args, **kwargs):
            print  additional, time.localtime()
            return func(*args, **kwargs)

        return wrapper
    return print_time_decorator


def print_time_decorator(func, additional=None):
    def wrapper(*args, **kwargs):
        print additional, time.localtime()
        return func(*args, **kwargs)

    return wrapper


def add_anything_time_print_decorator_factory_using_partial(a):
    return partial(print_time_decorator, additional=a)


@sample_time_print_decorator
def foo():
    print "foo called"


@add_hello_time_print_decorator
def say(words):
    print words


@add_anything_time_print_decorator_factory("Time now:")
def echo(words):
    print words


@add_anything_time_print_decorator_factory_using_partial("Want to know time?:")
def echo2(words):
    print words


@print_function_name
def what_is_my_name():
    pass


if __name__ == '__main__':
    foo()
    say("i am saying nothing")
    echo("Repeating")
    echo2("ham")
    what_is_my_name()
    pass

