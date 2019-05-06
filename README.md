# An anomaly detection algorithm POC

this repo contains a demo package 

RESTAPI: a Flask-based rest api wrapper around "anomaly", a subpackage containing a k-nearest neighbor anomaly detection algorithm

If you want to start the Flask aplication, you can simply type (in the api folder)

export FLASK_APP api
export FLASK_ENV development
flask run

this will start a flask server on 127.0.0.1:5000

exposing the following REST API:
 - GET /      -> http://127.0.0.1:5000/
 - GET /check -> http://127.0.0.1:5000/check?x=3.0&y=2.5
 - GET /check -> http://127.0.0.1:5000/check?x=30.0&y=2.5

 - POST http://127.0.0.1:5000/check
{
	"x": 2.0,
	"y": 3.0
}

 - POST http://127.0.0.1:5000/check
{"points":[
	{ 
		"x": 2.0,
		"y": 3.0
	},
	{ 
		"x": 4.0,
		"y": 5.0
	}
]}

### Note the the app DOES NOT accept relaxed json, so quotes are necessary

Poissibly you have to change the folder settings in the config.py file. Note that for one api call, a html page is generated containing a plot displaying the reference data overlaid with the anomaly status of a query point

dependencies:
* numpy
* scipy
* flask
* pandas
* matplotlib


Example data are found in the data folder

We have unit tests covering most of the exposed functionality; you find them in the api and anomaly subfolders

A jupyter notebook with a first prototype is found in the notebooks folder
