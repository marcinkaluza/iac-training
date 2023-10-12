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
        repo = cc.Repository(self, "repo", repository_name="app" )

        # 2) Create CodePipeline 
        # Enable docker for synth, 
        # set synth parameter to 
        # ShellStep("Synth",
        #   input=CodePipelineSource.code_commit(repo, branch="cicd"),
        #   commands=["npm install -g aws-cdk",
        #             "python -m pip install -r requirements.txt",
        #             "cdk synth"]
        # ) 
        # The documentation is availabel at:
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        pipeline = CodePipeline(self, "pipeline",
                                docker_enabled_for_synth=True,
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.code_commit(repo, branch="cicd"),
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]
                                                ))

        # 3) Add AppStage to the pipeline         
        pipeline.add_stage(stage=AppStage(self, "appstage"))

class AppStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApplicationStack(self, "ApplicationStack")