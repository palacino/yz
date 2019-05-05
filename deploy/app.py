from flask import Flask
from flask import request
from anomaly import moduleA
from configurator import Configurator

app = Flask(__name__)
app.config.from_object('config')
configurator = Configurator(app.config)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/class1/', methods=['GET'])
def test_class1():
    m1 = request.args.get('m1', type=int)
    m2 = request.args.get('m2', type=int)
    class1 = moduleA.Class1(m1, m2)
    response = class1.to_string()
    return response


def start_app():
    app.run()


if __name__ == '__main__':
    start_app()
