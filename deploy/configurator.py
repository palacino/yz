from OpenSSL import SSL


class Configurator:
    def __init__(self, config_object):
        self.__config_object = config_object

    def create_plot_generator(self):
        plot_folder = self.__config_object.get('PLOT_FOLDER')

        print('plot folder     = {}'.format(plot_folder))

    def create_ssl_context(self):
        security_folder = self.__config_object.get('SECURITY_FOLDER')
        print('security folder = {}'.format(security_folder))
        context = SSL.Context(SSL.SSLv23_METHOD)
        key_path = security_folder + '/key.pem'
        cert_path = security_folder + '/cert.pem'
        context.use_privatekey_file(key_path)
        context.use_certificate_file(cert_path)
