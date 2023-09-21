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
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    DENY_ALL_RESPONSE,
    APIGatewayAuthorizerRequestEvent,
    APIGatewayAuthorizerResponse,
    HttpVerb,
)

import json
import os
import jwt

from jwt import PyJWKClient

SERVICE_NAME = 'authorizer'

# Powertools setup
logger = Logger(service=SERVICE_NAME)
tracer = Tracer(service=SERVICE_NAME)

parameter_name = os.getenv('SSM_PARAMETER_NAME')
cognito_config = parameters.get_parameter(parameter_name, transform='json')

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@event_source(data_class=APIGatewayAuthorizerRequestEvent)
def lambda_handler(event: APIGatewayAuthorizerRequestEvent, context: LambdaContext):

    logger.debug(json.dumps(event.raw_event))

    try:
        # Extract authorization token, starting with headers and then query parameters
        token = event.get_header_value('Authorization', case_sensitive=False, default_value=None)

        if (token == None):
            token = event.query_string_parameters.get('Authorization', None)

        if (token == None):
            raise Exception('Missing authorization token')
        # Validate token and extract principalId claim

        url = cognito_config['url']
        aud = cognito_config['client_id']
        
        jwks_client = PyJWKClient(url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=aud,
            options={"verify_exp": requires_expiry_check()},
        )

        # Extract sub claim from the token
        principalId = data['sub']
        context = {}

        logger.info("Token valid. Subject: " + principalId)

        arn = event.parsed_arn

        # Create the response builder from parts of the `methodArn`
        # and set the logged in user id and context
        policy = APIGatewayAuthorizerResponse(
            principal_id=principalId,
            context=context,
            region=arn.region,
            aws_account_id=arn.aws_account_id,
            api_id=arn.api_id,
            stage=arn.stage,
        )

        policy.allow_all_routes()
        auth_response = policy.asdict()

        logger.debug(json.dumps(auth_response))

        return auth_response
    except Exception as e:
        logger.error(e)
        return DENY_ALL_RESPONSE
    
# This is debug time helper to allow for expiry check to be skipped
def requires_expiry_check():
    skip = os.getenv("SKIP_EXPIRY_CHECK")
    
    if skip == None or skip != "True":
        return True
    
    return False

