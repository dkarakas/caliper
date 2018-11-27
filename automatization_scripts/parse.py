#!/usr/bin/env python
import re
import matplotlib.pyplot as plt
import numpy as np
import glob, os
import sys


def extract_test(text_line):
    re_object = re.match(r".*(----test round [0-9]----).*|.*(###### testing '.*' ######).*", text_line)
    if re_object is None:
        return
    if re_object.group(1):
        print(re_object.group(1))
    if re_object.group(2):
        print(re_object.group(2))


def extract_transaction(text_line):
    re_object = re.match(
        r".*Submitted: (?P<submitted>[0-9]*) Succ: (?P<successful>[0-9]*) Fail:(?P<failed>[0-9]*) Unfinished:(?P<unfinished>[0-9]*)",
        text_line)
    if re_object is None:
        return
    print("Transactions are: Submitted: " + re_object.group("submitted") + " Successful: " + re_object.group(
        "successful"))


def extract_info(text_line):
    re_object = re.match(r"\| (?P<test_number>[0-9]*) *\| *(?P<test_type>open|query)"
                         r" *\| (?P<successful>[0-9]*) *\| *(?P<fail>[0-9]*) *"
                         r"\| *(?P<send_rate>[0-9]*) tps *\| *(?P<max_latency>[\.0-9]*) s *"
                         r"\| *(?P<min_latency>[\.0-9]*) s *\| *(?P<avg_latency>[\.0-9]*) s *"
                         r"\| *(?P<avg_througput>[0-9]*) tps *", text_line)

    if re_object is None:
        return None

    if re_object.group("test_type") == "query":  # for now ignore queries
        return None

    return re_object.group("send_rate"), re_object.group("max_latency"), re_object.group(
        "avg_latency"), re_object.group("avg_througput")


def plot_results(different_configs, data_for_plotting):
    input_rate = [x[0] for x in data_for_plotting[0]]  # input rate

    # Average throughput stuff
    max_avg_throughput = plot_format_data(input_rate, data_for_plotting, different_configs, 3)

    plt.ylim(0, max_avg_throughput)
    # plt.yticks(np.arange(0, max_avg_throughput + 5, step=100))
    plt.xticks(np.arange(min(input_rate), max(input_rate), step=100))

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel("Average Throughput")
    plt.xlabel("Input Rate")
    plt.savefig("average_throughput.png", bbox_inches="tight")

    plt.clf()
    # Average Latency
    max_avg_latency = plot_format_data(input_rate, data_for_plotting, different_configs, 2)
    plt.ylim(0, max_avg_latency)
    # plt.yticks(np.arange(0, max_avg_latency))
    plt.xticks(np.arange(min(input_rate), max(input_rate), step=100))

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel("Average Latency")
    plt.xlabel("Input Rate")
    plt.savefig("average_latency.png", bbox_inches="tight")

    plt.clf()
    # Maximum Latency
    max_max_latency = plot_format_data(input_rate, data_for_plotting, different_configs, 1)
    plt.ylim(0, max_max_latency)
    plt.yticks(np.arange(0, max_max_latency))
    plt.xticks(np.arange(min(input_rate), max(input_rate), step=100))

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel("Maximum Latency")
    plt.xlabel("Input Rate")
    plt.savefig("max_latency.png", bbox_inches="tight")


def plot_format_data(input_rate, data_to_plot, configs_to_plot, typeOfPlot):
    # typeOfPlot should be 1 - for max_latency , 2 - for avg_latency, 3 - for avg_throughput
    max_data = 0
    for i in range(0, len(configs_to_plot)):
        single_data = [data[typeOfPlot] for data in data_to_plot[i][:]]
        max_data = [data[typeOfPlot] for data in data_to_plot[i][:]].append(max_data)
        if i == 0:
            plt.plot(input_rate, single_data, label=configs_to_plot[i], marker='o', color='C0')
        elif i == 1:
            plt.plot(input_rate, single_data, label=configs_to_plot[i], marker='+', color='C0')
        elif i == 2:
            plt.plot(input_rate, single_data, label=configs_to_plot[i], marker='*', color='C0')
        elif i == 3:
            plt.plot(input_rate, single_data, label=configs_to_plot[i], marker='+', color='C1')
        elif i == 4:
            plt.plot(input_rate, single_data, label=configs_to_plot[i], marker='*', color='C1')
        elif i == 5:
            plt.plot(input_rate, single_data, label=configs_to_plot[i], marker='+', color='C1')
    return  max_data


def conv_to_float(tuple_of_data):
    input_rate = float(tuple_of_data[0])
    max_latency = float(tuple_of_data[1])
    avg_latency = float(tuple_of_data[2])
    avg_throughput = float(tuple_of_data[3])
    return input_rate, max_latency, avg_latency, avg_throughput


def generate_final_data(data_within_config):
    # calculates the averages
    new_data = [list(x) for x in data_within_config[0]]
    num_trails = len(data_within_config)

    for data_within_file in data_within_config[1:]:
        for i in range(len(new_data)):
            new_data[i][0] = (i + 1) * 50
            new_data[i][1] += data_within_file[i][1]
            new_data[i][2] += data_within_file[i][2]
            new_data[i][3] += data_within_file[i][3]

    for i in range(0, len(new_data)):
        new_data[i][1] = round(new_data[i][1] / num_trails, 1)
        new_data[i][2] = round(new_data[i][2] / num_trails, 1)
        new_data[i][3] = round(new_data[i][3] / num_trails, 1)

    return new_data[:16]


def parse_file_same_config(list_of_files):
    # list of files where only thing changing is the trail
    # it calculates the average and returns it as a list of lists

    data_of_config = []

    for file_to_process in list_of_files:
        with open(file_to_process) as outputFile:
            file_to_process = outputFile.readlines()

        data_config_spec_trail = []
        for i in range(0, len(file_to_process)):
            entry_of_file = extract_info(file_to_process[i])
            if entry_of_file is not None:
                entry_of_file = conv_to_float(entry_of_file)  # converting to floats
                data_config_spec_trail.append(entry_of_file)
        data_of_config.append(data_config_spec_trail)  # list containing each file's data and list of the actual data

    return generate_final_data(data_of_config)


if __name__ == "__main__":

    if len(sys.argv) != 3 or (sys.argv[1] != "dist" and sys.argv[1] != "scal") or not sys.argv[2].isdigit():
        print("Wrong inputs")
        print("First argument is either dist or scal")
        print("Second argument number of trails")
        print("Example: python parse.py dist 20")
        sys.exit(1)

    delimiter = "-"
    specify_trail = "t"
    file_extension = ".out"
    data_to_plot = []
    plot_labels = []
    if sys.argv[1] == "dist":
        types_of_dist = ["fixed", "poisson"]
        dist_configs = ["k1o2p1", "k3o2p1", "k5o2p1"]  # here we will specify all the configurations we will try
    else:
        types_of_dist = ["fixed", "poisson"]
        dist_configs = ["k1o2p1", "k1o2p2", "k1o2p3"]  # here we will specify all the configurations we will try

    for type_dist in types_of_dist:
        for config in dist_configs:
            config_files = []
            for trail in range(int(sys.argv[2])):
                config_files.append(type_dist + delimiter + config + delimiter + specify_trail + str(trail + 1) + file_extension)
            data_to_plot.append(parse_file_same_config(config_files))  # averaging across different trails
            plot_labels.append(type_dist + "-" + config)
    # print(data_to_plot)
    plot_results(plot_labels, data_to_plot)
