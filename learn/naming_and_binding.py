# -*- coding: UTF-8 -*-
__author__ = 'zonyu'


class A():
    """
    A scope defines the visibility of a name within a block.
    If a local variable is defined in a block, its scope includes that block.
    If the definition occurs in a function block, the scope extends to any blocks contained within the defining one,
    unless a contained block introduces a different binding for the name.
    The scope of names defined in a class block is limited to the class block;
    it does not extend to the code blocks of methods – this includes generator expressions since they are implemented
    using a function scope. This means that the following will fail:
    """
    a = 42
    #b = list(a + i for i in range(10))
    # while this works because list comprehension are not implemented using a function scope
    b = list([a + i for i in range(10)])


if __name__ == '__main__':
    pass