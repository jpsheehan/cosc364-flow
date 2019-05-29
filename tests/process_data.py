import csv
import sys
import os.path


def csvWrite(data):
    with open(sys.argv[2], 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)

    return


def openFile(Y):
    with open(os.path.join(sys.argv[1], '{0}.txt'.format(Y)), 'r') as in_file:
        stripped = [line.strip() for line in in_file.readlines()]
        lines = [line for line in stripped if line]
        data = []
        # Y
        data.append(Y)
        # elapsed time
        data.append(max(parseFile("elapsed_", lines)))
        # no of non-zero c links
        data.append(len(parseFile("c_", lines)))
        # no of non-zero d links
        data.append(len(parseFile("d_", lines)))
        # smallest_transit_node_load
        data.append(min(parseFile("l_", lines)))
        # largest_transit_node_load
        data.append(max(parseFile("l_", lines)))
        # highest cap c network
        data.append(max(parseFile("c_", lines)))
        # highest cap d network
        data.append(max(parseFile("d_", lines)))
        print(data)
        csvWrite(data)

        return


'''Returns a list of all values that start with the given string'''


def parseFile(string, lines):
    values = []
    for line in lines:
        if line.startswith(string):
            values.append(line.split()[1])

    return values


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: {0} <input directory> <csv file>".format(sys.argv[0]))
        exit(-1)

    openFile(3)
    openFile(4)
    openFile(5)
    openFile(6)
    openFile(7)
    openFile(8)
