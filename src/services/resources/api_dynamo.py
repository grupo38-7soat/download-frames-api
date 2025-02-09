from flask import request
from flask_restx import Namespace, Resource, reqparse
from loguru import logger
from config import Config
from repository.dynamo import DynamoRepository

AWS_REGION = Config.get('awsRegion')
DYNAMO_TABLE_NAME = Config.get('dynamoTableName')

dynamo_ns = Namespace(name='download-frames', description='API para download de frames')

parser = reqparse.RequestParser()
parser.add_argument('user', type=str, required=True, help='Nome do Usuario')
parser.add_argument('video_name', type=str, required=True, help='Nome do Video')
parser.add_argument('date', type=str, required=False, help='Dia da requisicao no formato yyyy-mm-dd')


def get_dynamo_repository():
    return DynamoRepository(region_name=AWS_REGION, table_name=DYNAMO_TABLE_NAME)

@dynamo_ns.route('/find-ids')
class ReadResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.dynamo_repository = kwargs.get('dynamo_repository', get_dynamo_repository())

    @dynamo_ns.expect(parser)
    def get(self):
        user = request.args.get('user')
        video_name = request.args.get('video_name')
        date = request.args.get('date')
        logger.info('Buscando dados - user: {} video_name: {} date: {}'.format(user, video_name, date))

        item = self.dynamo_repository.read_item(
            user=user,
            video_name=video_name,
            date=date
        )

        if item:
            return item, 200
        else:
            return {'message': 'Item not found'}, 404