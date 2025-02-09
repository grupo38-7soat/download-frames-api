from flask import Flask
from loguru import logger
from waitress import serve
from flask_restx import Api

from services.resources.api_dynamo import dynamo_ns

app = Flask(__name__)


class ApiService(object):
    HOST = '0.0.0.0'
    PORT = 3000

    def __init__(self):
        self.api = Api(app,
                       version='1.0',
                       title='API',
                       description='Descricao da API',
                       doc='/swagger/')

    def run(self):
        self.api.add_namespace(dynamo_ns)
        logger.info('Serving on http://{}:{}'.format(self.HOST, self.PORT))
        serve(app, host=self.HOST, port=self.PORT)