#!/bin/bash
# Luttappi installation scripti (alpha)
# Copyright 2018, Aswin Babu Karuvally

# get the current username
USER_NAME=`whoami`

# get the login user's name
LOGIN_NAME=`logname`

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

# copy the source file
cp luttappi.py /opt/luttappi/src/
chmod 755 /opt/luttappi/src/luttappi.py

# copy the service file
cp luttappi.service /lib/systemd/system/
chmod 644 /lib/systemd/system/luttappi.service

# setup luttappi to run as login user
sed -i '6s/root/$LOGIN_NAME/' /lib/systemd/system/luttappi.service

# enable the service
systemctl enable luttappi.service
systemctl start luttappi.service
