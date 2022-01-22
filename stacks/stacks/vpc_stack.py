from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)
from constructs import Construct

class StacksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "StacksQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        
        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")