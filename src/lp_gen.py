from lp_utils import perms, concat

template = """\
\\ COSC-364 Assignment 2, LP Output File

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


def get_nodes(x, y, z):
    """ Returns a tuple containing the source, transit and destination node ids as integers. """
    s = list(range(1, x + 1))
    t = list(range(1, y + 1))
    d = list(range(1, z + 1))
    return s, t, d


def get_demand_constraints(s, t, d):
    """ Returns a list of demand constraints. """
    return [' + '.join(["X_{0}{1}{2}".format(i, k, j) for k in t]) + ' = {0}'.format(2 * i + j)
            for (i, j) in perms([s, d])]


def get_source_transit_capacity_constraints(s, t, d):
    """ Returns a list of capacity constraints for the links between the source and transit nodes. """
    return \
        [' + '.join(["X_{0}{1}{2}".format(i, k, j) for j in d]) +
            ' - C_{0}{1} = 0'.format(i, k) for (i, k) in perms([s, t])]


def get_transit_destination_capacity_constraints(s, t, d):
    """ Returns a list of capacity constraints for the links between the transit and destination nodes. """
    return \
        [' + '.join(["X_{0}{1}{2}".format(i, k, j) for i in s]) +
            ' - D_{0}{1} = 0'.format(k, j) for (k, j) in perms([t, d])]


def get_transit_load_constraints(s, t, d):
    """ Returns the list of transit load constraints. """
    return [' + '.join(["X_{0}{1}{2}".format(i, k, j) for (i, j) in perms([s, d])]) +
            ' - l_{0} = 0'.format(k) for k in t]

def get_objective_function_load_constraints(s, t, d):
    """ Returns the list of objective function load constraints. """
    return []
    #return [' + '.join(["X_{0}{1}{2}".format(i, k, j) for (i, j) in perms([s, d])]) +
    #        ' - r <= 0' for k in t]

def get_binary_and_decision_variable_constraints(s, t, d):
    """ Returns the binary and decision variable constraints. """
    return []


def get_binary_constraints(s, t, d):
    """ Returns a list of binary variable constraints. """
    return [' + '.join(["U_{0}{1}{2}".format(i, k, j) for k in t]) + ' = 2'
            for (i, j) in perms([s, d])]


def get_binary_variables(s, t, d):
    """ Returns a list of binary variables. """
    return ["U_{0}{1}{2}".format(i, k, j) for (i, k, j) in perms([s, t, d])]


def get_non_negativity_constraints(s, t, d):
    """ Returns a list of non-negativity constraints. """
    return ["X_{0} >= 0".format(subscript) for subscript in concat(perms([s, t, d]))]


def generate_lp_file(x, y, z):
    """ Returns the LP file contents as per the project specification. """
    s, t, d = get_nodes(x, y, z)

    demand_constraints = '\n\t'.join(get_demand_constraints(s, t, d))
    source_transit_capacity_constraints = '\n\t'.join(
        get_source_transit_capacity_constraints(s, t, d))
    transit_destination_capacity_constraints = '\n\t'.join(
        get_transit_destination_capacity_constraints(s, t, d))
    non_negativity_constraints = '\n\t'.join(get_non_negativity_constraints(
        s, t, d))
    objective_function_load_constraints = '\n\t'.join(get_objective_function_load_constraints(s, t, d))
    transit_load_constraints = '\n\t'.join(
        get_transit_load_constraints(s, t, d))
    binary_and_decision_constraints = '\n\t'.join(get_binary_and_decision_variable_constraints(s, t, d))
    binary_variable_constraints = '\n\t'.join(get_binary_constraints(s, t, d))
    binary_variables = '\n\t'.join(get_binary_variables(s, t, d))

    return template.format(
        demand_constraints,
        source_transit_capacity_constraints,
        transit_destination_capacity_constraints,
        objective_function_load_constraints,
        transit_load_constraints,
        binary_and_decision_constraints,
        binary_variable_constraints,
        non_negativity_constraints,
        binary_variables)
