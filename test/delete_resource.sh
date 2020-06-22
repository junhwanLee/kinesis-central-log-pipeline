#!/bin/sh 

awslocal kinesis delete-stream --stream-name nginx-accesslog-stream 
awslocal s3api delete-bucket --bucket nginx-accesslog
awslocal iam delete-role --role-name kinesis-lambda-role
