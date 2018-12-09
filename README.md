# Luttappi 

Luttappi is a simple daemon to do temperature logging, plotting and analytics

## Introduction

Luttappi leverages the power of Python, lm-sensors, scikit-learn and bokeh
plotting library to log data from system temperature sensors, plot the
collected values and do generate useful information out of the collected data.

Luttappi is still far from being completed, and even lacks a built in web
server to output the data.

### Prerequisites

- A non ancient Linux Kernel
- Python 3.4 or greater 
- pip
- Virtualenv

### Installing

    $ python3 -m venv luttappi && cd luttappi

    $ git clone https://github.com/karuvally/luttappi.git src

    $ source bin/activate

    $ cd src 

    $ pip -r requirements 

## Built With

* [Python](http://www.python.org) - An awesome language
* [scikit-learn](http://www.python.org) - Machine Learning for Python
* [lm-sensors](https://github.com/lm-sensors/lm-sensors) - Get sensor values
* [Bokeh](https://bokeh.pydata.org) - Interactive plot for your data points


## Authors

* Aswin Babu Karuvally
* Navya Babu
* Phebe Raichal John

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details

