#!/bin/bash

[ -z "$S3_LOCATION" ] && { echo "S3_LOCATION is missing"; exit 1;  }
[ -z "$OUTPUT_FILE" ] && { echo "OUTPUT_FILE is missing"; exit 1;  }

aws s3 ls --recursive $S3_LOCATION > $OUTPUT_FILE
