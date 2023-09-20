from aws_cdk import (
    # Duration,
    Stack,
    BundlingOptions,
    aws_s3_assets as assets,
    aws_lambda as lambda_
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
