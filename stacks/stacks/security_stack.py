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
        
        self.bastion_sg = ec2.SecurityGroup(self, 'bastion_sg', # using self to attach rules
            security_group_name = 'bastion_sg',
            vpc=vpc,
            description = 'security group for bastion host',
            allow_all_outbound = True
        )
        
        self.bastion_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'SSH access') # ingress rule for bastion_sg
        
        lambda_role = iam.Role(self, 'lambdarole',
            assumed_by = iam.ServicePrincipal(service='lambda.amazonaws.com'),
            role_name = 'lambda-role',
            managed_policies = [iam.ManagedPolicy.from_aws_managed_policy_name(
                managed_policy_name = 'service-role/AWSLambdaBasicExecutionRole'
            )]
        )
        
        # inline policy
        lambda_role.add_to_policy( 
            statement = iam.PolicyStatement(
                actions = ['s3:*', 'rds:*'],
                resources = ['*']
            )
        )
        
        # SSM paramaters
        ssm.StringParameter(self, 'lambdasg-param',
            parameter_name = '/' + env_name + '/lambda-sg',
            string_value = lambda_sg.security_group_id
        )
        
        ssm.StringParameter(self, 'lambdarole-param-arn',
            parameter_name = '/' + env_name + '/lambda-role-arn',
            string_value = lambda_role.role_arn
        )
        
        ssm.StringParameter(self, 'lambdasg-param-name',
            parameter_name = '/' + env_name + '/lambda-role-name',
            string_value = lambda_role.role_name
        )
        