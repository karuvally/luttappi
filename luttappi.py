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
from bokeh.plotting import figure, output_file


# setup the logging system
def start_logging():
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
def read_log(date):
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
def plot_points(title, date, output):
    # get the data
    data = read_log(date)

    # set the output file
    output_file(os.path.join("static", output))

    # draw the plot
    plot = figure(title=title, x_axis_label="Time", y_axis_label="Temperature")
    plot.line(data["temp_values"], data["time_values"], legend="Celcius", line_width=2)


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


# log the sensors
def log_sensors(interval):
    while True:
        # get the temperature
        temperature_raw = subprocess.run(["sensors"], stdout=subprocess.PIPE)
        temperature_raw = temperature_raw.stdout.decode().split("\n")

        # extract temperature value
        for line in temperature_raw:
            strip_index = line.find("°")

            # get just the numbers
            if strip_index > 0:
                line = line[line.index(":")+1 : line.index("°")]
                temperature = line.lstrip()
                break

        # append sensor values to log
        write_to_log(temperature)

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

    # get current date
    date = time.strftime("%d-%m-%y")

    # draw simple plot
    plot_thread = threading.Thread(target=plot_points,
        args=["Temperature Plot", date, "plot.png"])
    plot_thread.start()

    # setup logging
    start_logging()


# call the main function
# main()

