import functools
import subprocess
import inspect


def get_lp_filename(x, y, z):
    """ Returns the filename that the LP data should be saved to. """
    return "problem_{0}_{1}_{2}.lp".format(x, y, z)


def run_cplex(filename):
    """ Runs cplex on the LP file. """
    subprocess.run(
        ['cplex', '-c', '"read {0}"'.format(filename), '"optimize"', '"display solution variables -"'])


def crange(first, last):
    """ Returns a list of characters between the two characters passed in (inclusive).
    >>> crange('A', 'C')
    ['A', 'B', 'C']
    >>> crange('A', 'A')
    ['A']
    """
    if ord(first) > ord(last):
        raise ValueError("last must come after first")

    else:
        return [chr(i) for i in range(ord(first), ord(last) + 1)]


def repeat(obj, n):
    """ Returns a list with obj repeated n times.
    >>> repeat(1, 1)
    [1]
    >>> repeat(42, 0)
    []
    >>> repeat(5, 4)
    [5, 5, 5, 5]
    >>> repeat([1, 2], 2)
    [[1, 2], [1, 2]]
    """
    return [obj for _ in range(n)]


def perms(lists):
    """ Returns all the permutations of the elements.
    >>> perms([])
    []
    >>> perms([['a', 'b', 'c']])
    [('a',), ('b',), ('c',)]
    >>> perms([['a', 'b', 'c'], ['x', 'y', 'z']])
    [('a', 'x'), ('a', 'y'), ('a', 'z'), ('b', 'x'), ('b', 'y'), ('b', 'z'), ('c', 'x'), ('c', 'y'), ('c', 'z')]
    """
    if len(lists) == 0:
        return []

    elif (len(lists) == 1):
        return [(x,) for x in lists[0]]

    else:
        return [(x,) + y for x in lists[0] for y in perms(lists[1:])]


def concat(permutations):
    """ Returns the permutations concatenated as strings.
    >>> concat(perms([['a', 'b', 'c']]))
    ['a', 'b', 'c']
    >>> concat(perms([['a', 'b', 'c'], ['x', 'y', 'z']]))
    ['ax', 'ay', 'az', 'bx', 'by', 'bz', 'cx', 'cy', 'cz']
    """
    return [functools.reduce(lambda x, y: x + str(y), p, '') for p in permutations]

def get_function_source(fn):
    src = inspect.getsource(fn)
    return src[str(src).index(':')+2:]

def get_lines(strings):
    return '\n\t'.join(strings)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
