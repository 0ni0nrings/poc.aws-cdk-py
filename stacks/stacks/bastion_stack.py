from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)
from constructs import Construct

class BastionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,vpc: ec2.Vpc, sg: ec2.SecurityGroup, **kwargs) -> None: # vpc & sg are newly added paramaters
        super().__init__(scope, construct_id, **kwargs)

        bastion_host = ec2.Instance(self, 'bastion-host',
            instance_type=ec2.InstanceType(
                instance_type_identifier='t2.micro'
            ),
            machine_image = ec2.AmazonLinuxImage(
                edition = ec2.AmazonLinuxEdition.STANDARD,
                generation = ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                virtualization = ec2.AmazonLinuxVirt.HVM,
                storage = ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            ),
            vpc=vpc,
            key_name='devops',
            vpc_subnets=ec2.SubnetSelection(
                subnet_type = ec2.SubnetType.PUBLIC
            ),
            security_group=sg
        )