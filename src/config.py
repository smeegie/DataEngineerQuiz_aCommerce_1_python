import os


config = {}

config['RAW_DIRECTORY'] = os.getenv('RAW_DIRECTORY', 'data/raw')
config['TRANSFORMED_DIRECTORY'] = os.getenv('TRANSFORMED_DIRECTORY', 'data/transformed')
