#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.vpc_stack import VPCStack # importing stack
from stacks.security_stack import SecurityStack
from stacks.bastion_stack import BastionStack
from stacks.kms_stack import KMSSStack
app = cdk.App()

vpc_stack = VPCStack(app, 'vpc') # initializing stack with name of CFN template, in this case vpc
security_stack = SecurityStack(app, 'security-stack', vpc=vpc_stack.vpc) # second parameter is name of CFN stack
bastion_stack = BastionStack(app, 'bastion', vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)
kms_stack = KMSSStack(app, 'kms') # second parameter is name of CFN stack

app.synth()