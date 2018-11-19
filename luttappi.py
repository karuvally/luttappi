#!/usr/bin/env python3
# luttappi, alpha release

# import the serious stuff
import csv
import os
import pwd
import pathlib
import sys


# generate the config directory path
def get_config_dir():
    # get the current username
    user = pwd.getpwduid(os.getuid())[0]

    # generate path
    config_dir = os.path.join("/home", user, ".config", "luttappi")

    # return path
    return config_dir


# check if essential files exist
def initialize_system():
    # get config_dir path
    config_dir = get_config_dir()

    # exit if lm_sensors not present
    if not os.path.isfile("/usr/bin/sensors"):
        print("fatal! lm_sensors not found")
        sys.exit(1)

    # create config_dir if not present
    if not os.isdir(config_dir):
        try:
            pathlib.Path(config_dir).mkdir(parents=True, exist_ok=True)
        except:
            print("fatal! configuration directory cannot be created")
            sys.exit(1)
    
    # initialize config_file if not present


# the main function
def main():
    # create files if they do not exist
    initialize_system()

    # log sensors in separate thread

    # start the web server


# call the main function
main()
