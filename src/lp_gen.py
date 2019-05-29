from lp_utils import perms, concat, get_lines, get_function_source

# Change these variables to alter the behaviour of the LP file generator
PATH_SPLIT = 2
DEMAND_FLOW = lambda i, j: 2 * i + j

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
    objective_function_load_constraints = get_lines(get_objective_function_load_constraints(s, t, d))
    transit_load_constraints = get_lines(
        get_transit_load_constraints(s, t, d))
    binary_and_decision_constraints = get_lines(get_binary_and_decision_variable_constraints(s, t, d))
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
