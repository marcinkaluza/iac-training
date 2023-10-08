from aws_cdk import (
    Stack,
    BundlingOptions,
    RemovalPolicy,
    CfnOutput,
    aws_s3_assets as assets,
    aws_s3_deployment as deployment,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_dynamodb as dynamo,
    aws_apigateway as api,
    aws_cognito as cognito,
)
from constructs import Construct

import os.path

dirname = os.path.dirname(__file__)


class ApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Create assets for the code of the comments-service.
        # The path of your asset shouild be set to f"{dirname}/comments-service/src/dist".
        # set bundling to:
        # BundlingOptions(
        #     image=lambda_.Runtime.PYTHON_3_10.bundling_image,
        #     command=["bash",
        #              "-c",
        #              "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
        #             ],
        #     security_opt="no-new-privileges:true",
        #     network="host"
        # )
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_assets/Asset.html#asset
        comments_service_asset = None

        # 2. Create dynamo db table for storing comments.
        # The table name should be set to "Comments", partition key should
        # be a numeric field "imageId" and the sort key should be a string field "commentId".
        # Also set the table's removal policy to DESTROY
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html#aws_cdk.aws_dynamodb.Table
        comments_table = None

        # 3. Create lambda functions named "comments-service".
        # The handler should be set to "app.lambda_handler", runtime tu Pythoin 3.10
        # and code should come from the bucket containing your lambda asset
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        comments_service = None

        # 4. Grant the comments service access read & write access to the table
        # created in step 2. using one of the grant* methods

        # 5. Create API Gateway lambda integration.
        # Set the handler to comments service from step 3. Allow test invocations
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        comments_service_integration = None

        # 6. Create REST API gateway. Set the default integration to one created in step 5.
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/RestApi.html
        apigateway = None

        # 7. Add a resource named "api" to the REST api created in step 6.
        root = None
        # 8. Add a resource named "comments" to the resource created in step 7.
        comments = None

        # 9. Create S3 bucket to hold the asssets for cloudfront distribution
        # set bucket encryption to S3_MANAGED, allow auto delete of objects and
        # set removal policy to DESTROY
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html#bucket
        website_bucket = None

        # 10. Create cloudfront distribution to host the website
        # Set the default root object to "index.html" and default behavior to S3 origin pointing to
        # the bucket created in step 9.
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudfront/Distribution.html#distribution
        distribution = None

        # 11. Add behaviour for the API to cloudfront distribution
        # The path pattern should be set to "/api/*"
        # caching policy should be set to CACHING_DISABLED,
        # origin request policy should be set to ALL_VIEWER_EXCEPT_HOST_HEADER,
        # allowed methods should be set to ALLOW_ALL
        # and the origin should be set to RestApiOrigin pointing to the API gateway created in step 6.

        # 12. Create asset containing web application's code. You need to follow README.md instructions in
        # order to build the application first. The asset's path should be set to f"{dirname}/website/dist"
        # THe documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_assets/Asset.html#asset
        website_assets = None

        # 13. Create bucket deployment
        # The deployment will copy and unzip the web app assets to the cloudfront distribution's bucket. Set the
        # soiurce of the deployment to website asset's (from step 12.) bucket and object key. Set the destination bucket to the
        # website bucket from step 9. Set the distribution to the distribution created in step 10 and distribution paths to ["/*"]
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_deployment/BucketDeployment.html#bucketdeployment

        # 14. Create cognito user pool
        # set sign in aliases to {"email": True} and enable self signup
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/UserPool.html#userpool
        pool = None
        # 15. Add a client to the user pool created in step 14.
        client = None

        # 16. Create user pool authorizer
        # Set the user pool of the authorizer to the pool created in step 14.
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/CognitoUserPoolsAuthorizer.html#cognitouserpoolsauthorizer
        auth = None

        # 17. Add a GET method to the API resource created in step 8.

        # 18. Add a POST method to the API resource created in step 8. Set the authorization type to COGNITO
        # and authorizer to once created in step 16.

        # 19: Create outputs for:
        #  - Cloudfront Distribution's domain name (from step 10)
        #  - User pool ID (from step 14)
        #  - User pool client's ID (from step 15)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/CfnOutput.html#cfnoutput

        # 20. Congratulations! Now run "CDK synth" to verify everything works as expected
        # and follow it with "cdk deploy"
