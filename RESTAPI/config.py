class Production:
    # SECURITY_FOLDER = '/Users/lverbeke/Documents/software/security'  # if you want to use https
    REFERENCE_DATA_PATH = '../data/anomaly.csv'
    CLEAN_REFERENCE_DATA_PATH = '../data/clean_data.csv'
    KNN_SEARCH_TYPE = 'mykdtree'


class Test:
    # SECURITY_FOLDER = '/Users/lverbeke/Documents/software/security'  # if you want to use https
    REFERENCE_DATA_PATH = '../../data/anomaly.csv'
    CLEAN_REFERENCE_DATA_PATH = '../../data/clean_data.csv'
    KNN_SEARCH_TYPE = 'mykdtree'
