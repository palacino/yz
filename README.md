# An anomaly detection algorithm POC

this repo contains two packages:
* anomaly: contains a k-nearest neighbor anomaly detection algorithm
* RESTAPI: a Flask-based rest api wrapper around "anomaly"

If you want to deploy the Flask aplication, you should copy the anomaly package inside the flask app folder, and simply type

python -m flask run in the api folder

dependencies:
* numpy
* scipy
* flask
* pandas
* matplotlib


Example data are found in the data folder

Both packages have unit tests covering most of the exposed functionality

A jupyter notebook with a first prototype is found in the notebooks folder
