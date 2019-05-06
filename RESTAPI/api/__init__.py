from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from api.configurator import Configurator
from api.inputprocessor import InputProcessor
import os
import numpy as np


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
    app = Flask(__name__)
    app.testing = testing

    app.config.from_object(config)
    Configurator.set_app(app)
    cleanup_temp_folder()

    @app.route('/', methods=['GET'])
    def hello_world():
        return 'Hello world from Flask!'

    @app.route('/check', methods=['GET'])
    def check_point_get():
        try:
            x = request.args.get('x', type=float)
            y = request.args.get('y', type=float)
            output_format = request.args.get('format', default='json', type=str)

            is_anomaly, score, message, query_time = Configurator.get_anomaly_detector().detect_anomaly([x, y])
            if output_format == 'json':
                return jsonify({'is_anomaly': is_anomaly, 'score': score, 'message': message, 'query_time': query_time})
            elif output_format == 'html':
                data = Configurator.get_anomaly_detector().data()
                plot_generator = Configurator.get_plot_generator()
                unique_file_name, title, caption = plot_generator.generate_anomaly_plot(data, np.array([[x, y]]),
                                                                                        np.array([is_anomaly]),
                                                                                        np.array([score]))
                return render_template('simpleplot.html', plot_url=unique_file_name, plot_caption=caption,
                                       plot_title=title)
            else:
                return jsonify(
                    {'is_anomaly': -1, 'score': -1.0, 'message': 'unknown output format: {}'.format(output_format),
                     'query_time': -1.0})
        except Exception as e:
            print(e)
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
