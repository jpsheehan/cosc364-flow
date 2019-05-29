import csv
import sys
import os.path
import numpy as np

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
    return list(map(lambda d: d["len_c_links"] + d["len_d_links"], data))


def get_transit_load_spread(data):
    return list(map(lambda d: d["max_load"] - d["min_load"], data))


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


def save_num_nonzero_links_plot(filename, data):
    """ Saves a plot of the number of non-zero links. """
    plt.bar(get_Y(data), get_len_nonzero_links(data))
    plt.xlabel("Y")
    plt.ylabel("")
    plt.title("Number of Non-Zero Link Capacities")
    plt.savefig(filename)
    plt.close()


def save_transit_load_spread_plot(filename, data):
    """ Saves a plot of the transit load spread. """
    plt.bar(get_Y(data), get_transit_load_spread(data))
    plt.xlabel("Y")
    plt.ylabel("Load")
    plt.title("Transit Node Load Spread")
    plt.savefig(filename)
    plt.close()


def save_highest_capacity_links_plot(filename, data):
    """ Saves a plot of the transit load spread. """
    width = 0.4
    Ys = np.array(get_Y(data))
    cs = plt.bar(Ys, get_max_cap_c(data), width, label="$C_{ik}$")
    ds = plt.bar(Ys + width, get_max_cap_d(data), width, label="$D_{kj}$")
    plt.xticks(Ys + width / 2, map(lambda x: int(x), Ys))
    plt.legend(handles=[cs, ds])
    plt.xlabel("Y")
    plt.ylabel("Link Capacity")
    plt.title("Highest Link Capacities")
    plt.savefig(filename)
    plt.close()


def get_data_from_csv(csv_filename):
    """ Returns an array of dictionaries containing the CSV data. """
    with open(csv_filename, newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=[
                                    "Y", "time", "len_c_links", "len_d_links", "min_load", "max_load", "max_cap_c", "max_cap_d"])
        rows = []
        for row in csv_reader:
            if csv_reader.line_num == 1:
                continue
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
