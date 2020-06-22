#!/bin/sh 

## 
# * prerequires 
#  - docker 
#  - localstack 
#  - awslocal
# create kinesis stream 
#  $ kinesis-stream (awslocal kinesis create-stream --stream-name nginx-accesslog-stream --shard-count 1)
# create s3 bucket 
#  $ awslocal s3 mb s3://kinesis-nginx-accesslog 
# create lambda 
#  $ awslocal iam create-role --role-name lambda-role --assume-role-policy-document file://init/AWSLambdaKinesisExecutionRole.json

# list buckets 
# $ aws s3api list-buckets 

# get role arn 
# $ ROLE_ARN_TEMP=`awslocal iam get-role --role-name lambda-role | grep "Arn" | awk '{print $2}' | cut -d',' -f1`
#
# $ awslocal lambda create-function --function-name KinesisEventToS3 --zip-file fileb://init/function.zip --handler kinesis_event_to_s3.handler --runtime python3.8 --role arn:aws:iam::000000000000:role/lambda-role 

# AWS lambda & kinesis stream mapping
# awslocal lambda create-event-source-mapping --function-name KinesisEventToS3 --event-source  arn:aws:kinesis:us-east-1:000000000000:stream/nginx-accesslog-stream  --batch-size 100 --starting-position LATEST

# s3 ls 
# awslocal s3 ls s3://kinesis-nginx-accesslog --recursive

# s3 get contents 
#  aws --endpoint-url http://localhost:4566 s3api get-object --bucket kinesis-nginx-accesslog --key 2020/05/27/15/39_nginx_access_log.json  mydata.out

# show s3 bucket list
# $ awslocal s3 ls kinesis-nginx-accesslog --recursive --human-readable 

# upload function 
# $ awslocal lambda update-function-code --function-name KinesisEventToS3 --zip-file fileb://init/function.zip 
