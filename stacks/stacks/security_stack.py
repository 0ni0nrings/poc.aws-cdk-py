from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)
from constructs import Construct

class SecurityStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name") or "serverless"
        env_name = self.node.try_get_context("env") or "dev"
        
        lambda_sg = ec2.SecurityGroup(self, 'lambda_sg',
            security_group_name = 'lambda_sg',
            vpc=vpc,
            description = 'security group for lambda function',
            allow_all_outbound = True
        )