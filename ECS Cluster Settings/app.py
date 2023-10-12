#!/usr/bin/env python3

from aws_cdk import core

from ecsgraviton.ecsgraviton_stack import EcsGravitonStack


app = core.App()
EcsGravitonStack(app, "ecsgraviton")

app.synth()
