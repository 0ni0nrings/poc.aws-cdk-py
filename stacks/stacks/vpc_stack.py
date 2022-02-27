from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)
from constructs import Construct

class VPCStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name") or "serverless"
        env_name = self.node.try_get_context("env") or "dev"
        
        self.vpc = ec2.Vpc(self, 'devVPC',
            cidr = "172.32.0.0/16",
            max_azs = 2,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            subnet_configuration = [
                ec2.SubnetConfiguration(
                    name = 'Public',
                    subnet_type = ec2.SubnetType.PUBLIC,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'Private',
                    subnet_type = ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask = 24
                ),
                ec2.SubnetConfiguration(
                    name = 'Isolated',
                    subnet_type = ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask = 24
                )
            ],
            nat_gateways = 1
        )
        
        priv_subnets =[]
        for subnet in self.vpc.private_subnets:
            priv_subnets.append(subnet.subnet_id)
        print(f"{priv_subnets}")
        
        count=1
        for priv_sub in priv_subnets:
            ssm.StringParameter(self, 'private-subnet-' + str(count),
                string_value = priv_sub,
                parameter_name = '/' + env_name + '/private-subnet-' + str(count)
            )
            count += 1
        