# Luttappi 

Luttappi is a simple daemon to do temperature plotting and analytics

## Introduction

Luttappi leverages the power of Python, lm-sensors, scikit-learn and Pyplot
to log data from system temperature sensors, plot the collected values and do
machine learning. Luttappi uses a non-supervised algorithm called K-Means
Clustering to cluster the logged values and thereby find where the system
temperatures usually lie.

### Prerequisites

- A non ancient Linux Kernel
- Python 3.4 or greater 
- pip
- Virtualenv

### Installing

    $ python3 -m venv luttappi && cd luttappi

    $ git clone https://github.com/karuvally/project_green.git src

    $ source bin/activate

    $ cd src 

    $ pip -r requirements 

## Built With

* [Python](http://www.python.org) - An awesome language
* [scikit-learn](http://www.python.org) - Machine Learning for Python


## Authors

* Aswin Babu Karuvally
* Navya Babu
* Phebe Raichal John

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details

