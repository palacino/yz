# An anomaly detection algorithm POC

this repo contains a demo package 

RESTAPI: a Flask-based rest api wrapper around "anomaly", a subpackage containing a k-nearest neighbor anomaly detection algorithm

If you want to start the Flask aplication, you can simply type

python -m flask run 

in the api folder

dependencies:
* numpy
* scipy
* flask
* pandas
* matplotlib


Example data are found in the data folder

We have unit tests covering most of the exposed functionality; you find them in the api and anomaly subfolders

A jupyter notebook with a first prototype is found in the notebooks folder
