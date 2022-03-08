from aws_cdk import (
    # Duration,
    Stack,
    aws_kms as kms,
    aws_ssm as ssm,
)
from constructs import Construct
from cdk_ec2_key_pair import KeyPair

class KMSSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name") or "serverless"
        env_name = self.node.try_get_context("env") or "dev"

        self.kms_rds = kms.Key(self, 'rdskey',
            description = '{}-key-rds'.format(prj_name),
            enable_key_rotation = True,
        )
        self.kms_rds.add_alias(
            alias_name = 'alias/{}-key-rds'.format(prj_name)
        )

        ssm.StringParameter(self, 'rdskey-param',
            string_value = self.kms_rds.key_id,
            parameter_name = '/' + env_name + '/rds-kms-key'
        )