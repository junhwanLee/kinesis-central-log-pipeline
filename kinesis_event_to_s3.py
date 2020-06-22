from __future__ import print_function
import json
import base64
import re
import boto3
import os 
from dateutil.parser import parser
from datetime import datetime

BUCKET_NAME='nginx-accesslog'
ACCESS_KEY='my-localstack-key'
SECRET_KEY='my-localstack-key'
ENDPOINT_URL='http://{}:4566'.format(os.environ['LOCALSTACK_HOSTNAME'])
REGION_NAME='us-east-1'


def handler(event, context):
	result = ""
	for record in event['Records']:
		#Kinesis data is base64 encoded so decode here
		payload=base64.b64decode(record["kinesis"]["data"]) 

		payload = eval(payload)

		if 'message' in payload:
			log_dict = parse_access_log(payload['message'])
			result += json.dumps(log_dict) + "\n"

	print ("result : {}".format(result))
	if result != "":
		upload_log_to_s3(result)


def upload_log_to_s3(body):
	s3 = boto3.client(
			's3',
			endpoint_url=ENDPOINT_URL
			)

	body = bytes(body, 'utf-8')
	now = datetime.now() 
	key = datetime.strftime(now, '%Y/%m/%d/%H/nginx_access_log_%M%S')
	key = "{}.json".format(key)
	s3.put_object(Bucket=BUCKET_NAME, Body=body, Key=key)



def parse_access_log(log):
	lineformat = re.compile( r"""(?P<remoteaddr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - (?P<remoteuser>.+) \[(?P<timelocal>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(?P<method>.+) )(?P<url>.+)(http\/[1-2]\.[0-9]")) (?P<statuscode>\d{3}) (?P<bytessent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<useragent>.+)["])""", re.IGNORECASE)
	data = re.search(lineformat, log)

	if data: 
		datadict = data.groupdict()
		#json_log = json.dumps(data.groupdict())
		
		return dict(data.groupdict())
	return None


if __name__ == '__main__': 
	print ('main')
	
	ENDPOINT_URL = 'http://localhost:4566'
	
	kinesis_event = "{'Records': [{'eventID': 'shardId-000000000000:49607324827115984088664622990943431398965320679772127234', 'eventSourceARN': 'arn:aws:kinesis:us-east-1:000000000000:stream/nginx-accesslog-stream', 'kinesis': {'data': 'eyJtZXNzYWdlIjoiMTcyLjIyLjAuMSAtIC0gWzI3L01heS8yMDIwOjAwOjQ3OjQzICswMDAwXSBcIkdFVCAvIEhUVFAvMS4xXCIgMzA0IDAgXCItXCIgXCJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV80KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODMuMC40MTAzLjYxIFNhZmFyaS81MzcuMzZcIiBcIi1cIiJ9Cg==', 'partitionKey': '6a19126ffdbbceab8ab9e84ab7a066fe', 'sequenceNumber': '49607324827115984088664622990943431398965320679772127234'}}, {'eventID': 'shardId-000000000000:49607324827115984088664622990944640324784935308946833410', 'eventSourceARN': 'arn:aws:kinesis:us-east-1:000000000000:stream/nginx-accesslog-stream', 'kinesis': {'data': 'eyJtZXNzYWdlIjoiMTcyLjIyLjAuMSAtIC0gWzI3L01heS8yMDIwOjAwOjQ3OjQ2ICswMDAwXSBcIkdFVCAvIEhUVFAvMS4xXCIgMzA0IDAgXCItXCIgXCJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV80KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvODMuMC40MTAzLjYxIFNhZmFyaS81MzcuMzZcIiBcIi1cIiJ9Cg==', 'partitionKey': '877d104948b46d0fd933be7bbe6d144e', 'sequenceNumber': '49607324827115984088664622990944640324784935308946833410'}}]}"

	_event = eval(kinesis_event)
	handler(_event, None)
