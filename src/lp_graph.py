# lp_graph.py
#
# COSC364 Assignment 2
# 30/05/2019
# Written by Will Cowper, Jesse Sheehan

import csv
import sys
import os.path

try:
    import numpy as np
except:
    print("Error: could not load 'numpy'. Install with 'pip install numpy' and then try again.")
    exit(-1)


try:
    import matplotlib.pyplot as plt
except:
    print("Error: could not load 'matplotlib'. Install with 'pip install matplotlib' and then try again.")
    exit(-1)


def get_data(data, key):
    return list(map(lambda d: d[key], data))


def get_time(data):
    return get_data(data, "time")


def get_len_nonzero_links(data):
    return get_data(data, "len_links")


def get_transit_load_spread(data):
    return get_data(data, "load_spread")


def get_max_cap_c(data):
    return get_data(data, "max_cap_c")


def get_max_cap_d(data):
    return get_data(data, "max_cap_d")


def get_Y(data):
    return get_data(data, "Y")


def save_execution_time_plot(filename, data):
    """ Saves a plot of execution time. """
    plt.bar(get_Y(data), get_time(data))
    plt.xlabel("Y")
    plt.ylabel("Time (ms)")
    plt.title("CPLEX Execution Time")
    plt.savefig(filename)
    plt.close()
    print("Saved '{}'".format(filename))


def save_num_nonzero_links_plot(filename, data):
    """ Saves a plot of the number of non-zero links. """
    plt.bar(get_Y(data), get_len_nonzero_links(data))
    plt.xlabel("Y")
    plt.ylabel("")
    plt.title("Number of Non-Zero Link Capacities")
    plt.savefig(filename)
    plt.close()
    print("Saved '{}'".format(filename))


def save_transit_load_spread_plot(filename, data):
    """ Saves a plot of the transit load spread. """
    plt.bar(get_Y(data), get_transit_load_spread(data))
    plt.xlabel("Y")
    plt.ylabel("Load")
    plt.title("Transit Node Load Spread")
    plt.savefig(filename)
    plt.close()
    print("Saved '{}'".format(filename))


def save_highest_capacity_links_plot(filename, data):
    """ Saves a plot of the transit load spread. """
    width = 0.4
    Ys = np.array(get_Y(data))
    cs = plt.bar(Ys, get_max_cap_c(data), width, label="$c_{ik}$")
    ds = plt.bar(Ys + width, get_max_cap_d(data), width, label="$d_{kj}$")
    plt.xticks(Ys + width / 2, map(lambda x: int(x), Ys))
    plt.legend(handles=[cs, ds])
    plt.xlabel("Y")
    plt.ylabel("Link Capacity")
    plt.title("Highest Link Capacities")
    plt.savefig(filename)
    plt.close()
    print("Saved '{}'".format(filename))


def get_data_from_csv(csv_filename):
    """ Returns an array of dictionaries containing the CSV data. """
    with open(csv_filename, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=[
                                    "Y", "time", "len_links", "load_spread", "max_cap_c", "max_cap_d"])
        rows = []
        for row in csv_reader:
            d = {}
            for key in row:
                d[key] = float(row[key])
            rows.append(d)
        return rows


def convert_csv_to_images(csv_filename, output_folder):
    """ Converts the data from the CSV into a set of graphs. """
    data = get_data_from_csv(csv_filename)
    base_filename = os.path.splitext(os.path.join(
        output_folder, os.path.basename(csv_filename)))[0]

    save_execution_time_plot(base_filename + "_time.png", data)
    save_num_nonzero_links_plot(base_filename + "_num_nonzero_links.png", data)
    save_transit_load_spread_plot(
        base_filename + "_transit_load_spread.png", data)
    save_highest_capacity_links_plot(
        base_filename + "_highest_capacity_links.png", data)


def print_usage():
    print("Usage: {0} <csv file> <output folder>")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        exit(-1)

    convert_csv_to_images(sys.argv[1], sys.argv[2])
