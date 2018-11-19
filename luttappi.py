#!/usr/bin/env python3
# luttappi, alpha release

# import the serious stuff
import csv
import os
import pwd


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
    pass # debug

    # get config_dir path

    # create config_dir if not present
    
    # create config_file if not present


# the main function
def main():
    # create files if they do not exist
    initialize_system()

    # log sensors in separate thread

    # start the web server


# call the main function
main()
