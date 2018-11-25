#!/usr/bin/env python
import re
import matplotlib.pyplot as plt
import np
import glob, os

def extract_test(text_line):
    re_object = re.match(r".*(----test round [0-9]----).*|.*(###### testing '.*' ######).*", text_line)
    if re_object is None:
        return
    if re_object.group(1):
        print(re_object.group(1))
    if re_object.group(2):
        print(re_object.group(2))


def extract_transaction(text_line):
    re_object = re.match(r".*Submitted: (?P<submitted>[0-9]*) Succ: (?P<successful>[0-9]*) Fail:(?P<failed>[0-9]*) Unfinished:(?P<unfinished>[0-9]*)", text_line)
    if re_object is None:
        return
    print("Transactions are: Submitted: " + re_object.group("submitted") + " Successful: " + re_object.group("successful"))

def extract_info(text_line):
    re_object = re.match(r"\| (?P<test_number>[0-9]*) *\| *(?P<test_type>open|query)"
                         r" *\| (?P<successful>[0-9]*) *\| *(?P<fail>[0-9]*) *"
                         r"\| *(?P<send_rate>[0-9]*) tps *\| *(?P<max_latency>[\.0-9]*) s *"
                         r"\| *(?P<min_latency>[\.0-9]*) s *\| *(?P<avg_latency>[\.0-9]*) s *"
                         r"\| *(?P<avg_througput>[0-9]*) tps *", text_line)

    if re_object is None:
        return None

    if re_object.group("test_type") == "query":#for now ignore queries
        return None

    return re_object.group("send_rate"), re_object.group("max_latency"), re_object.group("avg_latency"), re_object.group("avg_througput")
    # print("Test number is " + re_object.group("test_number") + " and the type is " + re_object.group("test_type"))
    # print("failed transactions is " + re_object.group("successful") + " succ transactions is " + re_object.group("fail"))
    # print("send rate was " + re_object.group("send_rate") + " max latency was " + re_object.group("max_latency"))
    # print("min latency was " + re_object.group("min_latency") + " max latency was " + re_object.group("avg_latency"))
    # print("avg througput" + re_object.group("avg_througput"))


def plot_results(name_file, data_to_plot):
    input_rate = [x[0] for x in data_to_plot] #input rate
    max_latency = [x[1] for x in data_to_plot] #max_latency
    avg_latency = [x[2] for x in data_to_plot] #avg latency
    avg_throughput = [x[3] for x in data_to_plot] #avg throughput

    #converting to list of ints
    input_rate = list(map(float, input_rate))
    max_latency = list(map(float, max_latency))
    avg_latency = list(map(float, avg_latency))
    avg_throughput = list(map(float, avg_throughput))

    plot_avg_throughput(name_file, input_rate, avg_throughput)
    plot_latency_avg(name_file, input_rate, avg_latency)
    plot_latency_avg(name_file, input_rate, max_latency)


def plot_avg_throughput(name_file,input_rate, avg_throughput):
    plt.plot(input_rate, avg_throughput, label=name_file)
    plt.ylim(0, max(avg_throughput))
    plt.ylim(0, max(avg_throughput))
    plt.yticks(np.arange(0, max(avg_throughput) + 5, step=100))
    plt.xticks(np.arange(min(input_rate), max(input_rate) + 51, step=50))

    plt.legend(loc='lower right')
    plt.ylabel("Average Throughput")
    plt.xlabel("Input Rate")
    plt.show()


def plot_latency_avg(name_file, input_rate, avg_latency):
    plt.plot(input_rate, avg_latency, label=name_file)
    plt.ylim(0, max(avg_latency))
    plt.yticks(np.arange(0, max(avg_latency) + 5))
    plt.xticks(np.arange(min(input_rate), max(input_rate) + 51, step=50))

    plt.legend(loc='lower right')
    plt.ylabel("Average Latency")
    plt.xlabel("Input Rate")
    plt.show()

def plot_latency_max(name_file, input_rate, max_latency):
    plt.plot(input_rate, max_latency, label=name_file)
    plt.ylim(0, max(max_latency))
    plt.yticks(np.arange(0, max(max_latency) + 5))
    plt.xticks(np.arange(min(input_rate), max(input_rate) + 51, step=50))

    plt.legend(loc='lower right')
    plt.ylabel("Maximum Latency")
    plt.xlabel("Input Rate")
    plt.show()


if __name__ == "__main__":
    list_of_files = []
    for file in os.listdir("."):
        if file.endswith(".out"):
            list_of_files.append(file)
    print(list_of_files)

    for file in list_of_files:
        with open(file) as outputFile:
            file = outputFile.readlines()

        data_to_plot = []
        for i in range(0, len(file)):
            temp_data = extract_info(file[i])
            if temp_data is not None:
                data_to_plot.append(temp_data)

        print(data_to_plot)
    # plot_results("2org-2peers", data_to_plot)

