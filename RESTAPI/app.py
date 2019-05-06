from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from configurator import Configurator
from inputprocessor import InputProcessor
import os

app = Flask(__name__, template_folder='./templates')
app.config.from_object('config')
configurator = Configurator(app)
plot_generator = configurator.create_plot_generator()
anomaly_detector = configurator.create_anomaly_detector()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/check', methods=['GET'])
def check_point_get():
    try:
        x = request.args.get('x', type=float)
        y = request.args.get('y', type=float)
        is_anomaly, score, message, query_time = anomaly_detector.detect_anomaly([x, y])
        return jsonify({'is_anomaly': is_anomaly, 'score': score, 'message': message, 'query_time': query_time})
    except Exception:
        return jsonify({'is_anomaly': -1, 'score': -1.0, 'message': 'bad request', 'query_time': -1.0})


@app.route('/check', methods=['POST'])
def check_point_post():
    try:
        req_data = request.get_json()
        point_data = InputProcessor.build_point_list_from_json(req_data)
        is_anomaly, score, message, query_time = anomaly_detector.check_list(point_data)
        return jsonify({'is_anomaly': list(is_anomaly), 'score': list(score), 'message': list(message),
                        'query_time': list(query_time)})
    except Exception:
        return jsonify({'is_anomaly': -1, 'score': -1.0, 'message': 'bad request', 'query_time': -1.0})


# @app.route('/randomplot/', methods=['GET'])
# def generate_random_plot():
#     noise_type = request.args.get('type', type=str)
#     n = request.args.get('n', type=int)
#     scale = request.args.get('scale', type=int)
#     uniform_noise = FeatureGenerator.generate(noise_type, n, scale)
#     plot_url, plot_title, plot_caption = plot_generator.generate_plot(uniform_noise, 'uniform data', 'uniform data')
#     return render_template('simpleplot.html', plot_url=plot_url, plot_title=plot_title,
#                            plot_caption=plot_caption)


def cleanup_temp_folder():
    temp_folder = configurator.temp_folder()
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


def start_app():
    app.run()


cleanup_temp_folder()

if __name__ == '__main__':
    start_app()
