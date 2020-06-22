import boto3 
import json

ENDPOINT_URL='http://localhost:4566'
KINESIS_NAME='nginx-accesslog-stream'
BUCKET_NAME='nginx-accesslog'
IAM_ROLE_NAME='kinesis-lambda-role'
FUNCTION_NAME='KinesisAccessLogToS3'

def create_kinesis_stream(): 
	client = boto3.client('kinesis', endpoint_url=ENDPOINT_URL)
	response = client.create_stream(StreamName=KINESIS_NAME, ShardCount=1)
	return response


def create_s3_bucket():
	client = boto3.client('s3', endpoint_url=ENDPOINT_URL)
	response = client.create_bucket(Bucket=BUCKET_NAME) 
	return response

def create_role():
	assume_role_policy_document = json.dumps(
			{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "kinesis:DescribeStream",
                        "kinesis:DescribeStreamSummary",
                        "kinesis:GetRecords",
                        "kinesis:GetShardIterator",
                        "kinesis:ListShards",
                        "kinesis:ListStreams",
                        "kinesis:SubscribeToShard",
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "s3:*"
                    ],
                    "Resource": "*"
                }
            ]
        }
	)

	client = boto3.client('iam', endpoint_url=ENDPOINT_URL)
	response = client.create_role(
			RoleName=IAM_ROLE_NAME, 
			AssumeRolePolicyDocument = assume_role_policy_document
			)
	return response


def create_lambda():
	role_client = boto3.client('iam', endpoint_url=ENDPOINT_URL)
	response = role_client.get_role(RoleName=IAM_ROLE_NAME)
	role_arn = response['Role']['Arn']

	with open('function.zip', 'rb') as f:
		zipped_code = f.read()

	client = boto3.client('lambda', endpoint_url=ENDPOINT_URL)
	response = client.create_function(
			FunctionName=FUNCTION_NAME,
			Runtime='python3.8',
			Role=role_arn, 
			Handler='kinesis_event_to_s3.handler',
			Code=dict(ZipFile=zipped_code),
			)

	# create event source mapping 
	kinesis_client = boto3.client('kinesis', endpoint_url=ENDPOINT_URL)
	response = kinesis_client.describe_stream(StreamName=KINESIS_NAME)
	# get kinesis arn 
	source_arn = response['StreamDescription']['StreamARN']
	response = client.create_event_source_mapping(
			EventSourceArn=source_arn, 
			FunctionName=FUNCTION_NAME,
			)


def create_resource():
	create_kinesis_stream()
	create_s3_bucket()
	create_role()
	create_lambda()


if __name__=='__main__': 
	create_resource()

