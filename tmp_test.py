import re


def func():
    try:
        return 1
    finally:
        return 2

print func()