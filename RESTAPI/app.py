from flask import Flask
from flask import request
from flask import render_template
from configurator import Configurator
from anomaly.featuregenerator import FeatureGenerator
import os

app = Flask(__name__, template_folder='./templates')
app.config.from_object('config')
configurator = Configurator(app)
plot_generator = configurator.create_plot_generator()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/demoplot/', methods=['GET'])
def generate_plot():
    plot_url, plot_title, plot_caption = plot_generator.generate_demo()
    return render_template('simpleplot.html', plot_url=plot_url, plot_title=plot_title,
                           plot_caption=plot_caption)


@app.route('/randomplot/', methods=['GET'])
def generate_random_plot():
    noise_type = request.args.get('type', type=str)
    n = request.args.get('n', type=int)
    scale = request.args.get('scale', type=int)
    uniform_noise = FeatureGenerator.generate(noise_type, n, scale)
    plot_url, plot_title, plot_caption = plot_generator.generate_plot(uniform_noise, 'uniform data', 'uniform data')
    return render_template('simpleplot.html', plot_url=plot_url, plot_title=plot_title,
                           plot_caption=plot_caption)


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
