from flask import Flask
from flask import request
from flask import jsonify
from api.configurator import Configurator
from api.inputprocessor import InputProcessor
import os


def cleanup_temp_folder():
    temp_folder = Configurator.temp_folder()
    print('cleaning up temp folder: {}'.format(temp_folder))
    print('current root folder: {}'.format(os.getcwd()))
    try:
        for file in os.listdir(temp_folder):
            if file.endswith('.jpg'):
                full_path = os.path.join(temp_folder, file)
                print(full_path)
                os.remove(full_path)
    except OSError as e:
        print('Failed with: {}'.format(e.strerror))


def create_app(config='config.Production', testing=False):
    print('using configuration {}, testing={}'.format(config, testing))
    app = Flask(__name__, template_folder='./templates')
    app.testing = testing

    app.config.from_object(config)
    Configurator.set_app(app)
    cleanup_temp_folder()

    @app.route('/',methods=['GET'])
    def hello_world():
        return 'Hello world from Flask!'

    @app.route('/check', methods=['GET'])
    def check_point_get():
        try:
            x = request.args.get('x', type=float)
            y = request.args.get('y', type=float)
            is_anomaly, score, message, query_time = Configurator.get_anomaly_detector().detect_anomaly([x, y])
            return jsonify({'is_anomaly': is_anomaly, 'score': score, 'message': message, 'query_time': query_time})
        except Exception:
            return jsonify({'is_anomaly': -1, 'score': -1.0, 'message': 'bad request', 'query_time': -1.0})

    @app.route('/check', methods=['POST'])
    def check_point_post():
        try:
            req_data = request.get_json()
            point_data = InputProcessor.build_point_list_from_json(req_data)
            is_anomaly, score, message, query_time = Configurator.get_anomaly_detector().check_list(point_data)
            return jsonify({'is_anomaly': list(is_anomaly), 'score': list(score), 'message': list(message),
                            'query_time': list(query_time)})
        except Exception:
            return jsonify({'is_anomaly': -1, 'score': -1.0, 'message': 'bad request', 'query_time': -1.0})

    return app
