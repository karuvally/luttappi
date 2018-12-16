#!/usr/bin/env python3
# luttappi, alpha release

# import the serious stuff
import csv
import os
import pwd
import pathlib
import sys
import json
import threading
import csv
import time
import subprocess
import datetime
import logging
from bokeh.plotting import figure, output_file, save, gridplot
from bottle import get, static_file, run


# serve the output
@get("/")
def serve_output():
    # get config directory path
    config_dir = get_config_dir()

    # get current date
    date = time.strftime("%d-%m-%y")

    # get log and output file timestamps
    log_timestamp = os.path.getmtime(os.path.join(config_dir, "logs", date))
    out_timestamp = os.path.getmtime(os.path.join(config_dir, "output.html"))

    # if newer log, plot
    if log_timestamp > out_timestamp:
        plot_points("Temperature Log on " + date, date, "output.html")

    return static_file("output.html", root=config_dir)


# setup the logging system
def start_logging():
    # essential variables
    config_dir = get_config_dir()

    # define logger format
    format_string = "[%(asctime)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # configure the logger
    logging.basicConfig(
        filename = os.path.join(config_dir, "log"),
        level = logging.DEBUG,
        format = format_string,
        datefmt = date_format
    )

    # print logs to stderr
    logging.getLogger().addHandler(logging.StreamHandler())
    
    # log initial messages
    logging.info("Luttappi (alpha) is starting up")
    logging.info("System passed initial checks")


# read from sensor log
def read_temp_log(date):
    # get the config directory
    config_dir = get_config_dir()

    # generate log file path
    log_file = os.path.join(config_dir, "logs", date)

    # extract the values
    with open(log_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        temp_values = []
        time_values = []
        for row in csv_reader:
            temp_values.append(float(row[0]))
            time_values.append(row[1])

    # return the values
    return{
        "temp_values": temp_values,
        "time_values": time_values
    }


# draw plot from given data
def plot_points(plot_title, date, output):
    # get config directory path
    config_dir = get_config_dir()

    # get the data
    data = read_temp_log(date)

    # prepare dummy x_values
    x_values = [x for x in range(len(data["temp_values"]))]

    # set the output file
    output_file(os.path.join(config_dir, output))

    # initialize the plot
    plot = figure(
        title = plot_title,
        x_axis_label = "Time (HH:MM:SS)",
        y_axis_label = "Temperature (°C)",
    )

    # prepare the plot
    plot.line(
        x = x_values,
        y = data["temp_values"],
        line_width = 2
    )

    # pair x_values with time_values
    x_axis_labels = {}
    for i in range(len(x_values)):
        x_axis_labels.update({x_values[i]: data["time_values"][i]})

    # set the labels
    plot.xaxis.major_label_overrides = x_axis_labels

    # force the plot to fill the screen
    plot = gridplot([[plot]], sizing_mode="stretch_both")

    # delete older plot, save the new plot
    os.remove(os.path.join(config_dir, output))
    save(plot)


# write to the sensor log
def write_to_log(value):
    # get configuration directory
    config_dir = get_config_dir()

    # generate timestamp
    log_name = time.strftime("%d-%m-%y")
    current_time = time.strftime("%H:%M:%S")

    # write to the log
    with open(os.path.join(config_dir, "logs", log_name), "a") as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow([value, current_time])


# log the sensors, debug: can we make this more pythonic?
def log_sensors(interval):
    while True:
        temperature = 0

        # get two temperature readings
        for i in range(2):
            temperature_raw = subprocess.run(
                ["sensors"], stdout=subprocess.PIPE
            )
            temperature_raw = temperature_raw.stdout.decode().split("\n")

            # extract temperature value
            for line in temperature_raw:
                strip_index = line.find("°")

                # get just the numbers
                if strip_index > 0:
                    line = line[line.index(":")+1 : line.index("°")]
                    temperature += float(line.lstrip())
                    break

            # sleep ten seconds
            sleep(10)

        # append mean of sensor values to log
        write_to_log(temperature/2)

        # sleep "interval" seconds
        time.sleep(interval)


# retrieve configuration
def read_configuration(key):
    # get configuration directory
    config_dir = get_config_dir()
    
    # read configuration from file
    with open(os.path.join(config_dir, "config")) as config_file:
        configuration = json.loads(config_file.read())

    # return specified value
    if key in configuration:
        return configuration[key]
    else:
        return None


# store configuration
def write_configuration(key, value):
    # get the configuration directory
    config_dir = get_config_dir()

    # read configuration file
    with open(os.path.join(config_dir, "config")) as config_file:
        configuration = json.loads(config_file.read())
    
    # update the configuration
    configuration.update({key: value})

    # write new configuration to file
    with open(os.path.join(config_dir, "config"), "w") as config_file:
        config_file.write(json.dumps(configuration))


# generate the config directory path
def get_config_dir():
    # get the current username
    user = pwd.getpwuid(os.getuid())[0]

    # generate path
    config_dir = os.path.join("/home", user, ".config", "luttappi")

    # return path
    return config_dir


# check if essential files exist
def initialize_system():
    # get config_dir path
    config_dir = get_config_dir()
    log_dir = os.path.join(config_dir, "logs")

    # exit if lm_sensors not present
    if not os.path.isfile("/usr/bin/sensors"):
        logging.critical("lm_sensors not found")
        sys.exit(1)

    # create config and log directories if not present
    if not os.path.isdir(log_dir):
        try:
            pathlib.Path(log_dir).mkdir(parents=True, exist_ok=True)
        except:
            logging.critical("config directory cannot be created")
            sys.exit(1)
    
    # initialize config_file if not present
    if not os.path.isfile(os.path.join(config_dir, "config")):
        configuration = {
            "update_interval": 300
        }

        with open(os.path.join(config_dir, "config"), "w") as config:
            config.write(json.dumps(configuration))


# the main function
def main():
    # create files if they do not exist
    initialize_system()

    # read interval value
    interval = int(read_configuration("update_interval"))

    # log sensors in separate thread
    sensor_thread = threading.Thread(target=log_sensors, args=[interval])
    sensor_thread.start()

    # setup logging
    start_logging()

    # start the web server
    run(host="0.0.0.0", port=9000, debug=True)


# call the main function
main()

