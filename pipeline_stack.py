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

        repo = cc.Repository(self, "repo", repository_name="app" )

        pipeline = CodePipeline(self, "pipeline",
                                docker_enabled_for_synth=True,
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.code_commit(repo, branch="cicd"),
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]
                                                ))
        
        pipeline.add_stage(stage=AppStage(self, "appstage"))

class AppStage(Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ApplicationStack(self, "TechuStack")