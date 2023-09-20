"""

Copyright 2023 Amazon.com, Inc. and its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

  http://aws.amazon.com/asl/

  or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

"""
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver, Response, content_types)
from decimal import Decimal
import json
import boto3
import uuid

from http import HTTPStatus
from munch import munchify
from boto3.dynamodb.conditions import Key
from jsonschema import validate, ValidationError
from schemas import assetSchema

# Constants
KEY_NAME = 'imageId'
TABLE_NAME = 'Comments'
DEFAULT_PATH = '/api/comments'
SERVICE_NAME = 'comments-service'

# Powertools setup
logger = Logger(service=SERVICE_NAME)
tracer = Tracer(service=SERVICE_NAME)
app = APIGatewayRestResolver()

# Initialize dynamo table
dynamodb = boto3.resource('dynamodb')
assets = dynamodb.Table(TABLE_NAME)

# Lambda handler


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.debug(json.dumps(event))
    return app.resolve(event, context)

# Create item


@app.post(DEFAULT_PATH)
@tracer.capture_method
def createItem():

    if app.current_event.is_base64_encoded:
        return error(HTTPStatus.BAD_REQUEST.value, 'Invalid API gateway configuration: Base64 encoded payload received.')

    item = json.loads(app.current_event.body, parse_float=Decimal)
    validate(instance=item, schema=assetSchema)

    item['commentId'] = str(uuid.uuid4())
    item['author'] = app.current_event.request_context.authorizer.claims["cognito:username"]

    response = assets.put_item(Item=item)

    return ok(item)


# Returns asset with particular id
@app.get(DEFAULT_PATH)
@tracer.capture_method
def getItem():

    id = app.current_event.get_query_string_value(
        name=KEY_NAME, default_value=None)

    response = assets.query(KeyConditionExpression=Key(
        KEY_NAME).eq(id), ConsistentRead=True)
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = assets.scan(
            ExclusiveStartKey=response['LastEvaluatedKey'], ConsistentRead=True)
        data.extend(response['Items'])

    return ok(data)

# Helper methods


def ok(payload):
    return Response(
        status_code=HTTPStatus.OK.value,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps(payload, cls=DecimalEncoder),
    )


def error(statusCode, message):
    return Response(
        status_code=statusCode,
        content_type=content_types.TEXT_PLAIN,
        body=message,
    )


# Encoder for serializing decimals
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(str(obj))
        return json.JSONEncoder.default(self, obj)
