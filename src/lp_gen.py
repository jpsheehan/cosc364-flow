
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
    {3}
END
"""


def generate_lp_file(x, y, z):
    """ Generates the LP file as per the project specification. """
    demand_constraints = ""
    capacity_constraints = ""
    non_negativity_constraints = ""
    binary_variables = ""
    return template.format(demand_constraints, capacity_constraints, non_negativity_constraints, binary_variables)
