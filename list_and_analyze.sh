#!/bin/bash

[ -z "$1" ] && { echo "Usage: $0 s3bucket/s3path"; exit 1; }

export S3_LOCATION=s3://$1
export OUTPUT_FILE=s3-list-output

./s3_list.sh || exit 1
./analyze.py "$OUTPUT_FILE" || exit 1
