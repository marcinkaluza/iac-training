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
        comments_service_asset = assets.Asset(self, "comments-service-asset",
                                              path=f"{dirname}/comments-service/src",
                                              bundling=BundlingOptions(
                                                  image=lambda_.Runtime.PYTHON_3_10.bundling_image,
                                                  command=["bash",
                                                           "-c",
                                                           "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                                                           ],
                                                  security_opt="no-new-privileges:true",
                                                  network="host"
                                              )
                                              )

        # 2. Create dynamo db table for storing comments.
        # The table name should be set to "Comments", partition key should
        # be a numeric field "imageId" and the sort key should be a string field "commentId".
        # Also set the table's removal policy to DESTROY
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html#aws_cdk.aws_dynamodb.Table
        comments_table = dynamo.Table(self, "comments-table",
                                      table_name="Comments",
                                      removal_policy=RemovalPolicy.DESTROY,
                                      partition_key=dynamo.Attribute(
                                          name="imageId",
                                          type=dynamo.AttributeType.NUMBER
                                      ),
                                      sort_key=dynamo.Attribute(
                                          name="commentId",
                                          type=dynamo.AttributeType.STRING
                                      ))

        # 3. Create lambda functions named "comments-service".
        # The handler should be set to "app.lambda_handler", runtime tu Pythoin 3.10
        # and code should come from the bucket containing your lambda asset
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        comments_service = lambda_.Function(self, "comments-service",
                                            function_name="comments-service",
                                            handler="app.lambda_handler",
                                            runtime=lambda_.Runtime.PYTHON_3_10,
                                            code=lambda_.Code.from_bucket(comments_service_asset.bucket, comments_service_asset.s3_object_key))

        # 4. Grant the comments service access read & write access to the table
        # created in step 2. using one of the grant* methods
        comments_table.grant_read_write_data(comments_service)

        # 5. Create API Gatewaylambda integration.
        # Set the handler to comments service from step 3. Allow test invocations
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        comments_service_integration = api.LambdaIntegration(
            handler=comments_service, allow_test_invoke=True)

        # 6. Create REST API gateway. Set the default integration to one created in step 5.
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/RestApi.html
        apigateway = api.RestApi(self, "api",
                                 default_integration=comments_service_integration
                                 )

        # 7. Add a resource named "api" to the REST api created in step 6.
        root = apigateway.root.add_resource("api")
        # 8. Add a resource named "comments" to the resource created in step 7.
        comments = root.add_resource("comments")

        # 9. Create S3 bucket to hold the asssets for cloudfront distribution
        # set bucket encryption to S3_MANAGED, allow auto delete of objects and
        # set removal policy to DESTROY
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html#bucket
        website_bucket = s3.Bucket(self, "website-bucket",
                                   encryption=s3.BucketEncryption.S3_MANAGED,
                                   auto_delete_objects=True,
                                   removal_policy=RemovalPolicy.DESTROY)

        # 10. Create cloudfront distribution to host the website
        # Set the default root object to "index.html" and default behavior to S3 origin pointing to
        # the bucket created in step 9.
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudfront/Distribution.html#distribution
        distribution = cloudfront.Distribution(self, "distribution",
                                               default_root_object="index.html",
                                               default_behavior=cloudfront.BehaviorOptions(
                                                   origin=origins.S3Origin(website_bucket))
                                               )

        # 11. Add behaviour for the API to cloudfront distribution
        # The caching policy should be set to CACHING_DISABLED, the origin request policy should be set to
        # ALL_VIEWER_EXCEPT_HOST_HEADER, and the origin should be set to RestApiOrigin pointing to the
        # API gateway created in step 6.
        distribution.add_behavior(path_pattern="/api/*",
                                  cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                                  allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                                  origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                                  origin=origins.RestApiOrigin(apigateway))

        # 12. Create asset containing web application's code. You need to follow README.md instructions in
        # order to build the application first. The asset's path should be set to f"{dirname}/website/dist"
        # THe documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_assets/Asset.html#asset
        website_assets = assets.Asset(self, "website-assets",
                                      bundling=BundlingOptions(
                                                  image=lambda_.Runtime.NODEJS_18_X.bundling_image,
                                                  command=["bash",
                                                           "-c",
                                                           "npm i && npm run build && cp -r ./dist/* /asset-output"
                                                           ],
                                                  security_opt="no-new-privileges:true",
                                                  network="host"
                                              ),
                                      path=f"{dirname}/website")

        # 13. Create bucket deployment
        # The deployment will copy and unzip the web app assets to the cloudfront distribution's bucket. Set the
        # soiurce of the deployment to website asset's (from step 12.) bucket and object key. Set the destination bucket to the
        # website bucket from step 9. Set the distribution to the distribution created in step 10 and distribution paths to ["/*"]
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_deployment/BucketDeployment.html#bucketdeployment
        deployment.BucketDeployment(self, "website-deployment",
                                    sources=[deployment.Source.bucket(
                                        website_assets.bucket, website_assets.s3_object_key)],
                                    destination_bucket=website_bucket,
                                    distribution=distribution,
                                    distribution_paths=["/*"])

        # 14. Create cognito user pool
        # set sign in aliases to {"email": True} and enable self signup
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/UserPool.html#userpool
        pool = cognito.UserPool(self, "Pool",
                                sign_in_aliases={"email": True},
                                self_sign_up_enabled=True)

        # 15. Add a client to the user pool created in step 14.
        client = pool.add_client("app-client")

        # 16. Create user pool authorizer
        # Set the user pool of the authorizer to the pool created in step 14.
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/CognitoUserPoolsAuthorizer.html#cognitouserpoolsauthorizer
        auth = api.CognitoUserPoolsAuthorizer(self, "authorizer",
                                              cognito_user_pools=[pool]
                                              )

        # 17. Add a GET method to the API resource created in step 8.
        comments.add_method("GET")

        # 18. Add a POST method to the API resource created in step 8. Set the authorization type to COGNITO
        # and authorizer to once created in step 16.
        comments.add_method("POST",
                            authorizer=auth,
                            authorization_type=api.AuthorizationType.COGNITO)

        # 19: Create outputs for:
        #  - Cloudfront Distribution's domain name (from step 10)
        #  - User pool ID (from step 14)
        #  - User pool client's ID (from step 15)
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/CfnOutput.html#cfnoutput
        CfnOutput(self, "website-url", value=distribution.domain_name)
        CfnOutput(self, "userpool-id", value=pool.user_pool_id)
        CfnOutput(self, "client-id", value=client.user_pool_client_id)
