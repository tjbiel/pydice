PyDice provides a simple set of tools for simulating die rolls.

***************
Sample Usage
***************
Simplest usage is rolling from a string. Patterns here are inspired by Sam Clements's dice module (https://github.com/borntyping/python-dice). ::

    import pydice
    
    # roll 3 six-sided dice
    r = pydice.roll('3d6')
    
    # get the sum of all the dice
    # e.g., 11
    r.total
    
    # or get the individual die results as a list
    # e.g., [4, 2, 5]
    r.faces

Also supports modifiers and top/bottom x dice. ::

    >>> # roll 6 six-sided dice, keep the top 3, and add 1 to the total
    >>> r = pydice.roll('6d6^3+1')
    >>> r.faces
    [6, 5, 5]
    >>> r.sum
    16
    >>> r.total
    17
    
You can inspect the individual Die objects in a roll. ::

    >>> r = pydice.roll('2d8')
    >>> r.dice
    [<Die (d8): faces=[1, 2, 3, 4, 5, 6, 7, 8], result=3>,
    <Die (d8): faces=[1, 2, 3, 4, 5, 6, 7, 8], result=2>]

Or get a collection of results in a dictionary for use elsewhere. ::

    >>> r = pydice.roll('2d10+2')
    >>> r.result
    {'throw_mod' : 2, 'sum': 8, 'total': 10, 'faces': [5, 3]}
