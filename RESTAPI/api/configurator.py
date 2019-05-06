# from OpenSSL import SSL
from api.plotgenerator import PlotGenerator
from anomaly.knnanomalydetector import KNNAnomalyDetector


class Configurator:
    __config_object = None
    __app_root_folder = None
    __anomaly_detector = None
    __plot_creator = None

    @staticmethod
    def set_app(app):
        Configurator.__config_object = app.config
        Configurator.__app_root_folder = app.root_path

    @staticmethod
    def temp_folder():
        return Configurator.__app_root_folder + '/static/temp'

    @staticmethod
    def static_folder():
        return Configurator.__app_root_folder + '/static'

    @staticmethod
    def get_plot_generator():
        if not Configurator.__plot_creator:
            Configurator.__plot_generator = PlotGenerator(Configurator.static_folder())

        return Configurator.__plot_generator

    # @staticmethod
    # def create_ssl_context():
    #     security_folder = Configurator.__config_object.get('SECURITY_FOLDER')
    #     print('security folder = {}'.format(security_folder))
    #     context = SSL.Context(SSL.SSLv23_METHOD)
    #     key_path = security_folder + '/key.pem'
    #     cert_path = security_folder + '/cert.pem'
    #     context.use_privatekey_file(key_path)
    #     context.use_certificate_file(cert_path)

    @staticmethod
    def get_anomaly_detector():
        if not Configurator.__anomaly_detector:
            ref_data = Configurator.__config_object.get('REFERENCE_DATA_PATH')
            search_type = Configurator.__config_object.get('KNN_SEARCH_TYPE')
            Configurator.__anomaly_detector = KNNAnomalyDetector(ref_data, search_type)

        return Configurator.__anomaly_detector
