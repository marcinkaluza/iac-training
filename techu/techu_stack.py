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


class TechuStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        comments_service_asset = assets.Asset(self, "comments-service-asset",
                                              path=f"{dirname}/comments-service/src",
                                              bundling=BundlingOptions(
                                                  image=lambda_.Runtime.PYTHON_3_10.bundling_image,
                                                  command=["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                                                           ],
                                                  security_opt="no-new-privileges:true",
                                                  network="host"
                                              )
                                              )

        # website_assets = assets.Asset(self, "website-assets",
        #                               path=f"{dirname}/website",
        #                               bundling=BundlingOptions(
        #                                   image=lambda_.Runtime.NODEJS_18_X.bundling_image,
        #                                   command=["bash", "-c", "npm ci && npm run build && cp -aur ./dist/* /asset-output"
        #                                            ],
        #                                   security_opt="no-new-privileges:false",
        #                                   network="host",
        #                                   user="root"
        #                               )
        #                               )

        website_assets = assets.Asset(self, "website-assets",
                                      path=f"{dirname}/website/dist")

        comments_table = dynamo.Table(self, "comments-table", table_name="Comments",
                                      partition_key=dynamo.Attribute(
                                          name="imageId",
                                          type=dynamo.AttributeType.NUMBER
                                      ),
                                      sort_key=dynamo.Attribute(
                                          name="commentId",
                                          type=dynamo.AttributeType.STRING
                                      ))
        # Comments service
        comments_service = lambda_.Function(self, "comments-service",
                                            function_name="comments-service",
                                            handler="app.lambda_handler",
                                            runtime=lambda_.Runtime.PYTHON_3_10,
                                            code=lambda_.Code.from_bucket(comments_service_asset.bucket, comments_service_asset.s3_object_key))

        comments_table.grant_read_write_data(comments_service)

        # API Gateway
        comments_service_integration = api.LambdaIntegration(
            handler=comments_service, allow_test_invoke=True)

        apigateway = api.RestApi(self, "api",
                                 default_integration=comments_service_integration
                                 )

        root = apigateway.root.add_resource("api")
        comments = root.add_resource("comments")

        website_bucket = s3.Bucket(self, "website-bucket",
                                   encryption=s3.BucketEncryption.S3_MANAGED,
                                   auto_delete_objects=True,
                                   removal_policy=RemovalPolicy.DESTROY)

        distribution = cloudfront.Distribution(self, "distribution",
                                               default_root_object="index.html",
                                               default_behavior=cloudfront.BehaviorOptions(
                                                   origin=origins.S3Origin(website_bucket))
                                               )

        deployment.BucketDeployment(self, "website-deployment",
                                    sources=[deployment.Source.bucket(
                                        website_assets.bucket, website_assets.s3_object_key)],
                                    destination_bucket=website_bucket,
                                    distribution=distribution,
                                    distribution_paths=["/*"])

        distribution.add_behavior(path_pattern="/api/*",
                                  cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,
                                  allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                                  origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER_EXCEPT_HOST_HEADER,
                                  origin=origins.RestApiOrigin(apigateway, ))

        # Cognito user pool
        pool = cognito.UserPool(self, "Pool",
                                sign_in_aliases={"email": True},
                                self_sign_up_enabled=True)
        client = pool.add_client("app-client",
                                 o_auth=cognito.OAuthSettings(
                                     flows=cognito.OAuthFlows(
                                         authorization_code_grant=True
                                     ),
                                     scopes=[cognito.OAuthScope.OPENID],
                                     callback_urls=[
                                         f'https://{distribution.distribution_domain_name}/', "http://localhost:3000/"],
                                     logout_urls=[
                                         f"https://{distribution.distribution_domain_name}/", "http://localhost:3000/"]
                                 )
                                 )

        auth = api.CognitoUserPoolsAuthorizer(self, "authorizer",
                                              cognito_user_pools=[pool]
                                              )

        comments.add_method("GET")
        comments.add_method("POST",
                            authorizer=auth,
                            authorization_type=api.AuthorizationType.COGNITO)

        CfnOutput(self, "website-url", value=distribution.domain_name)
        CfnOutput(self, "userpool-id", value=pool.user_pool_id)
        CfnOutput(self, "client-id", value=client.user_pool_client_id)
