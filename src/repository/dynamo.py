import os
import boto3
from loguru import logger
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr


class DynamoRepository:
    def __init__(self, region_name=None, table_name=None):
        self.region_name = region_name
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb',
                                       region_name=self.region_name ,
                                       aws_access_key_id=os.getenv('ACCESS_KEY'),
                                       aws_secret_access_key=os.getenv('SECRET_KEY')
                                       )
        self.table = self.dynamodb.Table(self.table_name)


    def read_item(self, user, video_name, date):
        try:
            filters = Attr("user").eq(user) & Attr("video_name").eq(video_name)

            if date:  # Se o parâmetro date foi passado, adicionamos ao filtro
                filters = filters & Attr("date").eq(date)

            items = []
            last_evaluated_key = None

            while True:
                scan_params = {"FilterExpression": filters}

                if last_evaluated_key:
                    scan_params["ExclusiveStartKey"] = last_evaluated_key

                response = self.table.scan(**scan_params)
                items.extend(response.get("Items", []))

                last_evaluated_key = response.get("LastEvaluatedKey")

                if not last_evaluated_key:
                    break
            logger.info(f"Item read: {items}")
            return items
        except ClientError as e:
            logger.exception(f"Error reading item: {e.response['Error']['Message']}")
            return None
