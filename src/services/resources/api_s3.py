import os
import boto3
from io import BytesIO

import jwt
import requests
from flask import request, Response
from flask_restx import Namespace, Resource, reqparse

from loguru import logger

from config import Config


AWS_REGION = Config.get('awsRegion')
S3_BUCKET_NAME = Config.get('bucketResult')

s3_ns = Namespace(name='download-frames', description='API para download de frames')

parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='Token da API de Usuário')
parser.add_argument('s3_file_name', type=str, required=True, help='Nome do Arquivo no S3')

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY'),
    aws_secret_access_key=os.getenv('SECRET_KEY'),
    region_name=AWS_REGION
)


@s3_ns.route('/find-ids')
class ReadResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    @s3_ns.expect(parser)
    def get(self):
        try:
            token = request.args.get('token')
            user = decode_jwt(token)

            if not user:
                raise ValueError("Erro ao obter os dados do usuário.")

            find_user = retrieve_user(user)

            if not find_user:
                raise ValueError("Usuário não encontrado.")

            filename = request.args.get('s3_file_name')

            logger.info('Baixando frame - user: {} filename: {}'.format(user, filename))

            file_obj = BytesIO()
            s3_client.download_fileobj(S3_BUCKET_NAME, f'results/{user}/{filename}', file_obj)
            file_obj.seek(0)

            return Response(
                file_obj.read(),
                content_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
        except Exception as e:
            logger.error(f"Erro ao baixar arquivo: {str(e)}")
            return {"error": str(e)}, 500


def retrieve_user(user_id):
    url = f'{os.getenv("USER_API_URL")}/usuarios/{user_id}'

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Retorna o conteúdo JSON da resposta
        else:
            return {"Erro ao obter os dados do usuário."}, 400

    except requests.exceptions.RequestException as e:
        # Em caso de erro na requisição
        return {"Erro": str(e)}, 500


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=['HS256'], options={"verify_signature": False})
        user_id = payload.get("id")
        if user_id:
            return user_id
    except jwt.ExpiredSignatureError as e:
        raise ValueError(f'Erro ao obter o token: {e}')
    except jwt.InvalidTokenError as e:
        raise ValueError(f'Erro ao obter o token: {e}')
    except Exception as e:
        raise ValueError(f'Erro ao obter o token: {e}')

