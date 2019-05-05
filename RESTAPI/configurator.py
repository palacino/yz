from OpenSSL import SSL
from plotgenerator import PlotGenerator


class Configurator:
    def __init__(self, app):
        self.__config_object = app.config
        self.__app_root_folder = app.root_path

    def temp_folder(self):
        return self.__app_root_folder+'/static/temp'

    def create_plot_generator(self):
        plot_generator = PlotGenerator(self.__app_root_folder)
        return plot_generator

    def create_ssl_context(self):
        security_folder = self.__config_object.get('SECURITY_FOLDER')
        print('security folder = {}'.format(security_folder))
        context = SSL.Context(SSL.SSLv23_METHOD)
        key_path = security_folder + '/key.pem'
        cert_path = security_folder + '/cert.pem'
        context.use_privatekey_file(key_path)
        context.use_certificate_file(cert_path)
