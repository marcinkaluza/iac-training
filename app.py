#!/usr/bin/env python3
import os

import aws_cdk as cdk

from application.application_stack import ApplicationStack
from pipeline_stack import PipelineStack

app = cdk.App()

PipelineStack(app, "PipelineStack")


app.synth()
