import builtins
import typing
from aws_cdk import (
    Stack,
    Stage,
    aws_codecommit as cc
)

from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from constructs import Construct
from application.application_stack import ApplicationStack


class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # 1) Create code commit repository
        # Set repository name to something human readable like "app"
        # The documentation is available at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codecommit/Repository.html
        repo = None

        # 2) Create CodePipeline 
        # Enable docker for synth, 
        # set synth parameter to 
        # ShellStep("Synth",
        #   input=CodePipelineSource.code_commit(repo, branch="cicd"),
        #   commands=["npm install -g aws-cdk",
        #             "python -m pip install -r requirements.txt",
        #             "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\"",
        #             "cdk synth"]
        # ) 
        # The documentation is availabel at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        pipeline = None

        # 3) Once you have created pipeline and repository resources, deploy the app using by executing 'cdk deploy'
        
        # 4) Open CodeCommit console and copy the HTTPS clone url, add the repository as new remote by executing 
        # git remote add codecommit <URL>         

        # 5) Add AppStage to the pipeline         
        
        
        # 6) Commit your changes and push them to the CodeCommit repository by executing
        # git push codecommit cicd

class AppStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApplicationStack(self, "ApplicationStack")
