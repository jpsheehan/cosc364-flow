import csv
import sys
import os.path


def csvWrite(data):
    with open(sys.argv[2], 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)


def floatmap(enumerable):
    return list(map(lambda x: float(x), enumerable))


def openFile(Y):
    with open(os.path.join(sys.argv[1], '{0}.txt'.format(Y)), 'r') as in_file:
        stripped = [line.strip() for line in in_file.readlines()]
        lines = [line for line in stripped if line]
        data = []
        # Y
        data.append(Y)
        # elapsed time
        data.append(max(parseFile("elapsed_", lines)))
        # no of non-zero c and d links
        data.append(len(parseFile("c_", lines)) + len(parseFile("d_", lines)))
        # transit load spread (largest_transit_node_load - smallest_transit_node_load)
        data.append(max(floatmap(parseFile("l_", lines))) -
                    min(floatmap(parseFile("l_", lines))))
        # highest cap c network
        data.append(max(parseFile("c_", lines)))
        # highest cap d network
        data.append(max(parseFile("d_", lines)))
        csvWrite(data)


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

    # delete the CSV, otherwise we will append to it
    os.unlink(sys.argv[2])

    openFile(3)
    openFile(4)
    openFile(5)
    openFile(6)
    openFile(7)
    openFile(8)

    print("Saved CSV data to '{}'".format(sys.argv[2]))
