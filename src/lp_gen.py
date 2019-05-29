# lp_gen.py
#
# COSC364 Assignment 2
# 30/05/2019
# Written by Will Cowper, Jesse Sheehan

import inspect
import functools
import sys
import os.path

__TITLE__ = "COSC-364 Assignment 2 LP Generator"
__AUTHORS__ = [("Will Cowper", "81163265"), ("Jesse Sheehan", "53366509")]

# Change these variables to alter the behaviour of the LP file generator
PATH_SPLIT = 2


def DEMAND_FLOW(i, j): return 2 * i + j


TEMPLATE = """\
\\ {}, LP Output File
\\ Written by {}
\\ Parameters: X={}, Y={}, Z={}, Split={}, Demand={}

MINIMIZE
\tr

SUBJECT TO

\t\\ DEMAND CONSTRAINTS
\t{}

\t\\ CAPACITY CONSTRAINTS FOR LINKS BETWEEN SOURCE AND TRANSIT NODES
\t{}

\t\\ CAPACITY CONSTRAINTS FOR LINKS BETWEEN TRANSIT AND DESTINATION NODES
\t{}

\t\\ OBJECTIVE FUNCTION LOAD CONSTRAINTS
\t{}

\t\\ TRANSIT NODE LOAD CONSTRAINTS
\t{}

\t\\ BINARY VARIABLE AND DECISION VARIABLE CONSTRAINTS
\t{}

\t\\ BINARY VARIABLE CONSTRAINTS (ONLY 2 ACTIVE TRANSIT NODES)
\t{}

BOUNDS

\t\\ NON-NEGATIVITY CONSTRAINTS
\tr >= 0
\t{}

BIN

\t\\ BINARY VARIABLES
\t{}

END
"""

# DEFINE SOME UTILITY FUNCTIONS


def get_lp_filename(x, y, z):
    """ Returns the filename that the LP data should be saved to. """
    return "problem_{0}_{1}_{2}.lp".format(x, y, z)


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
    return src[str(src).index('return')+7:]


def get_lines(strings):
    return '\n\t'.join(strings)

# DEFINE SOME FUNCTIONS SPECIFIC TO THE PROBLEM


def get_nodes(x, y, z):
    """ Returns a tuple containing the source, transit and destination node ids as integers. """
    s = list(range(1, x + 1))
    t = list(range(1, y + 1))
    d = list(range(1, z + 1))
    return s, t, d


def get_demand_constraints(s, t, d):
    """ Returns a list of demand constraints. """
    return [' + '.join(["x_{0}{1}{2}".format(i, k, j) for k in t]) + ' = {0}'.format(DEMAND_FLOW(i, j))
            for (i, j) in perms([s, d])]


def get_source_transit_capacity_constraints(s, t, d):
    """ Returns a list of capacity constraints for the links between the source and transit nodes. """
    return \
        [' + '.join(["x_{0}{1}{2}".format(i, k, j) for j in d]) +
            ' - c_{0}{1} = 0'.format(i, k) for (i, k) in perms([s, t])]


def get_transit_destination_capacity_constraints(s, t, d):
    """ Returns a list of capacity constraints for the links between the transit and destination nodes. """
    return \
        [' + '.join(["x_{0}{1}{2}".format(i, k, j) for i in s]) +
            ' - d_{0}{1} = 0'.format(k, j) for (k, j) in perms([t, d])]


def get_transit_load_constraints(s, t, d):
    """ Returns the list of transit load constraints. """
    return [' + '.join(["x_{0}{1}{2}".format(i, k, j) for (i, j) in perms([s, d])]) +
            ' - l_{0} = 0'.format(k) for k in t]


def get_objective_function_load_constraints(s, t, d):
    """ Returns the list of objective function load constraints. """
    return [' + '.join(["c_{0}{1}".format(i, j) for i in s]) +
            ' - r <= 0' for j in d]


def get_binary_and_decision_variable_constraints(s, t, d):
    """ Returns the binary and decision variable constraints. """
    return ['{3} x_{0}{1}{2} - {4} u_{0}{1}{2} = 0'.format(i, k, j, PATH_SPLIT, DEMAND_FLOW(i, j)) for (i, k, j) in perms([s, t, d])]


def get_binary_constraints(s, t, d):
    """ Returns a list of binary variable constraints. """
    return [' + '.join(["u_{0}{1}{2}".format(i, k, j) for k in t]) + ' = {}'.format(PATH_SPLIT)
            for (i, j) in perms([s, d])]


def get_binary_variables(s, t, d):
    """ Returns a list of binary variables. """
    return ["u_{0}{1}{2}".format(i, k, j) for (i, k, j) in perms([s, t, d])]


def get_non_negativity_constraints(s, t, d):
    """ Returns a list of non-negativity constraints. """
    return ["x_{0}{1}{2} >= 0".format(i, k, j) for (i, k, j) in perms([s, t, d])] + ["c_{0}{1} >= 0".format(i, k) for (i, k) in perms([s, t])] + ["d_{0}{1} >= 0".format(k, j) for (k, j) in perms([t, d])]


def generate_lp_file(title, authors, x, y, z):
    """ Returns the LP file contents as per the project specification. """
    s, t, d = get_nodes(x, y, z)

    demand_constraints = get_lines(get_demand_constraints(s, t, d))
    source_transit_capacity_constraints = get_lines(
        get_source_transit_capacity_constraints(s, t, d))
    transit_destination_capacity_constraints = get_lines(
        get_transit_destination_capacity_constraints(s, t, d))
    non_negativity_constraints = get_lines(get_non_negativity_constraints(
        s, t, d))
    objective_function_load_constraints = get_lines(
        get_objective_function_load_constraints(s, t, d))
    transit_load_constraints = get_lines(
        get_transit_load_constraints(s, t, d))
    binary_and_decision_constraints = get_lines(
        get_binary_and_decision_variable_constraints(s, t, d))
    binary_variable_constraints = get_lines(get_binary_constraints(s, t, d))
    binary_variables = get_lines(get_binary_variables(s, t, d))

    return TEMPLATE.format(
        title,
        authors,
        x,
        y,
        z,
        PATH_SPLIT,
        get_function_source(DEMAND_FLOW),
        demand_constraints,
        source_transit_capacity_constraints,
        transit_destination_capacity_constraints,
        objective_function_load_constraints,
        transit_load_constraints,
        binary_and_decision_constraints,
        binary_variable_constraints,
        non_negativity_constraints,
        binary_variables)


# DEFINE SOME HELPERS FOR GETTING THE THING RUNNING

def print_version():
    print('{0} by {1}'.format(__TITLE__, get_author_string()))


def print_usage():
    print('Usage: {0} <x> <y> <z> [output directory]'.format(sys.argv[0]))


def get_problem_parameters():
    """ Returns a tuple containing the x, y and z parameters. """
    try:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        z = int(sys.argv[3])
    except:
        print_usage()
        exit(-1)

    if x <= 0:
        print("Error: x must be strictly positive")
        exit(-1)

    if x >= 10:
        print("Error: x must be less than ten")
        exit(-1)

    if y <= 0:
        print("Error: y must be strictly positive")
        exit(-1)

    if y >= 10:
        print("Error: y must be less than ten")
        exit(-1)

    if z <= 0:
        print("Error: z must be strictly positive")
        exit(-1)

    if z >= 10:
        print("Error: z must be less than ten")
        exit(-1)

    return x, y, z


def save_lp_file(filename, data):
    try:
        f = open(filename, 'w')
        f.write(data)
        f.close()
    except:
        print("Error: could not save file '{0}'".format(filename))
        exit(-1)


def get_author_string():
    return ', '.join(
        ["{0} ({1})".format(name, sid) for (name, sid) in __AUTHORS__])


def main():
    print_version()
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print_usage()
        exit(-1)
    else:
        output_dir = '.'
        if len(sys.argv) == 5:
            output_dir = sys.argv[4]

        x, y, z = get_problem_parameters()
        data = generate_lp_file(__TITLE__, get_author_string(), x, y, z)
        filename = os.path.join(output_dir, get_lp_filename(x, y, z))
        save_lp_file(filename, data)
        print("Success: saved as '{0}'".format(filename))


if __name__ == "__main__":
    main()
