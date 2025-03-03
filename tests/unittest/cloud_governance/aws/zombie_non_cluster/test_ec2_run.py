
import boto3
from moto import mock_ec2, mock_s3

from cloud_governance.common.clouds.aws.s3.s3_operations import S3Operations
from cloud_governance.policy.aws.ec2_run import EC2Run

AWS_DEFAULT_REGION = 'us-east-2'


@mock_ec2
def test_ec2_run():
    """
    This method test running ec2 instances
    @return:
    """
    region = AWS_DEFAULT_REGION
    ec2_client = boto3.client('ec2', region_name=region)
    default_ami_id = 'ami-03cf127a'
    ec2_client.run_instances(ImageId=default_ami_id, InstanceType='t2.micro', MaxCount=1, MinCount=1)
    ec2_run = EC2Run()
    ec2_run.set_dryrun(value='yes')
    ec2_run.set_policy(value='ec2_run')
    ec2_run.set_region(value=AWS_DEFAULT_REGION)
    assert 1 == len(ec2_run.run())


@mock_s3
@mock_ec2
def test_ec2_run_s3_upload():
    """
    This method test the data is upload t s3 or not
    @return:
    """
    region = AWS_DEFAULT_REGION
    ec2_client = boto3.client('ec2', region_name=region)
    default_ami_id = 'ami-03cf127a'
    ec2_client.run_instances(ImageId=default_ami_id, InstanceType='t2.micro', MaxCount=1, MinCount=1)
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_client.create_bucket(Bucket='test-upload-data', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    policy_output = 's3://test-upload-data/test'
    s3operations = S3Operations(region_name='us-east-1')
    ec2_run = EC2Run()
    ec2_run.set_dryrun(value='yes')
    ec2_run.set_policy(value='ec2_run')
    ec2_run.set_region(value=AWS_DEFAULT_REGION)
    assert s3operations.save_results_to_s3(policy='ec2_run', policy_output=policy_output, policy_result=ec2_run.run()) is None
