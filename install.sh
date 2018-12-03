#!/bin/bash
# Luttappi installation scripti (alpha)
# Copyright 2018, Aswin Babu Karuvally

# get the current username
USER_NAME=`whoami`

# exit if not root
if [ $USER_NAME != "root" ]
then
    echo "run script as root!"
    exit
fi

# setup virtualenv 
mkdir -p /opt/luttappi/src
python3 -m venv /opt/luttappi

# setup the libraries
source /opt/luttappi/bin/activate
pip install --upgrade pip
pip install wheel
pip install bottle
pip install matplotlib
deactivate

# get the login user's name
LOGIN_NAME=`logname`

# setup luttappi to run as login user

# copy the source file
cp luttappi.py /opt/luttappi/src/
chmod 755 /opt/luttappi/src/luttappi.py

# setup the service

