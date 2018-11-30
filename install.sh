#!/bin/bash
# Luttappi installation script
# Copyright 2018, Aswin Babu Karuvally

# get the current username
USER_NAME=`whoami`

# exit if not root
if [ $USER_NAME != "root" ]
then
    echo "run script as root!"
    exit
fi
