#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.vpc_stack import VPCStack # importing stack
from stacks.security_stack import SecurityStack
app = cdk.App()

vpc_stack = VPCStack(app, 'vpc') # initializing stack
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc) # second parameter is name of CFN stack


app.synth()