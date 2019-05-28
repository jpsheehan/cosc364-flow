from lp_utils import perms, concat

template = """\
\\ COSC-364 Assignment 2, LP Output File
MINIMIZE
    r
SUBJECT TO
    \\ DEMAND CONSTRAINTS
    {0}
    \\ CAPACITY CONSTRAINTS
    {1}
BOUNDS
    \\ NON-NEGATIVITY CONSTRAINTS
    {2}
BIN
    \\ BINARY VARIABLES
    {3}
END
"""


def get_nodes(x, y, z):
    """ Returns a tuple containing the source, transit and destination node ids as integers. """
    s = list(range(1, x + 1))
    t = list(range(1, y + 1))
    d = list(range(1, z + 1))
    return s, t, d


def get_demand_constraints(s, t, d):
    """ Returns a list of demand constraints. """
    return [' + '.join(["X_{0}{1}{2}".format(i, k, j) for k in t]) + ' = {0}'.format(2*i + j)
            for (i, j) in perms([s, d])]


def get_capacity_constraints(s, t, d):
    """ Returns a list of capacity constraints. """
    return []


def get_binary_variables(s, t, d):
    """ Returns a list of binary variables. """
    return []


def get_non_negativity_constraints(s, t, d):
    """ Returns a list of non-negativity constraints. """
    return ["X_{0} >= 0".format(subscript) for subscript in concat(perms([s, t, d]))]


def generate_lp_file(x, y, z):
    """ Returns the LP file contents as per the project specification. """
    s, t, d = get_nodes(x, y, z)

    demand_constraints = '\n\t'.join(get_demand_constraints(s, t, d))
    capacity_constraints = '\n\t'.join(get_capacity_constraints(s, t, d))
    non_negativity_constraints = '\n\t'.join(get_non_negativity_constraints(
        s, t, d))
    binary_variables = '\n\t'.join(get_binary_variables(s, t, d))
    return template.format(demand_constraints, capacity_constraints, non_negativity_constraints, binary_variables)
