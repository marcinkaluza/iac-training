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
    aws_cloudfront_origins as origins
)
from constructs import Construct

import os.path

dirname = os.path.dirname(__file__)


class TechuStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        asset = assets.Asset(self, "BundledAsset",
                             path=f"{dirname}/authorizer/src",
                             bundling=BundlingOptions(
                                 image=lambda_.Runtime.PYTHON_3_10.bundling_image,
                                 command=["bash", "-c", "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                                          ],
                                 security_opt="no-new-privileges:true",
                                 network="host"
                             )
                             )

        website = assets.Asset(self, "WebsiteAsset",
                               path=f"{dirname}/website",
                               bundling=BundlingOptions(
                                   image=lambda_.Runtime.NODEJS_18_X.bundling_image,
                                   command=["bash", "-c", "npm ci && npm run build && cp -aur ./dist/* /asset-output"
                                            ],
                                   security_opt="no-new-privileges:false",
                                   network="host",
                                   user="root"
                               )
                               )

        website_bucket = s3.Bucket(self, "website-bucket",
                                   encryption=s3.BucketEncryption.S3_MANAGED,
                                   auto_delete_objects=True,
                                   removal_policy=RemovalPolicy.DESTROY)

        distribution = cloudfront.Distribution(self, "Distribution",
                                               default_root_object="index.html",
                                               default_behavior=cloudfront.BehaviorOptions(
                                                   origin=origins.S3Origin(website_bucket))
                                               )

        deployment.BucketDeployment(self, "website-deployment",
                                    sources=[deployment.Source.bucket(
                                        website.bucket, website.s3_object_key)],
                                    destination_bucket=website_bucket,
                                    distribution=distribution,
                                    distribution_paths=["/*"])

        CfnOutput(self, "website_bucket_name",
                  value=website_bucket.bucket_name)
        CfnOutput(self, "assets_bucket_name", value=website.s3_bucket_name)
        CfnOutput(self, "assets_object_name", value=website.s3_object_key)
        CfnOutput(self, "website_url", value=distribution.domain_name)
