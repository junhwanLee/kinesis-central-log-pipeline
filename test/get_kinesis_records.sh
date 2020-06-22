#!/bin/sh 

STREAM_NAME="nginx-accesslog-stream"

SHARD_ITERATOR=$(awslocal kinesis get-shard-iterator --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON --stream-name $STREAM_NAME --query 'ShardIterator')

echo $SHARD_ITERATOR

awslocal kinesis get-records --shard-iterator "$SHARD_ITERATOR"
