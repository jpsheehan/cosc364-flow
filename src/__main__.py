import sys

from lp_gen import generate_lp_file
from lp_utils import get_lp_filename

__TITLE__ = "COSC-364 Assignment 2 LP Generator"
__AUTHORS__ = [("Will Cowper", "81163265"), ("Jesse Sheehan", "53366509")]


def print_version():
    print('{0} by {1}'.format(__TITLE__, get_author_string()))


def print_usage():
    print('Usage: {0} <x> <y> <z>'.format(sys.argv[0]))


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
    if len(sys.argv) != 4:
        print_usage()
        exit(-1)
    else:
        x, y, z = get_problem_parameters()
        data = generate_lp_file(__TITLE__, get_author_string(), x, y, z)
        filename = get_lp_filename(x, y, z)
        save_lp_file(filename, data)
        print("Success: saved as '{0}'".format(filename))


if __name__ == "__main__":
    main()
