import boto3
import json
import os
from os import environ
import re
import logging
import sys
import sentry_sdk
from sentry_sdk.integrations.logging import ignore_logger
sentry_sdk.init(dsn='https://2fee4ed938294813aeeb28f08e3614b8@sentry.io/1858927')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


UAP_SNS_TOPIC="arn:aws:sns:ap-southeast-2:416748369696:UAPSNS"

count=os.environ['AWS_BATCH_JOB_ARRAY_INDEX']
BUCKET='aws-batch-parameter'



session = boto3.Session(region_name='ap-southeast-2')
print dir(session)


try:
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET).download_file(KEY, '/tmp/%s.txt'%(KEY))
except Exception as e:
    raise ValueError('Error while downloading temmplate file %s from %s '%(aws-batch-parameter))
    logger.info(' ERROR while downloading template file')
finally:
    logger.info('Downloading Template Ended')

file=open('/tmp/%s.txt'%(KEY)).read().splitlines()
print(file[count])

line = file[count].split(' ')


source_bucket_key=str(line[0])
destination_bucket_key=str(line[1])
source_bucket_name=str(line[2])
destination_bucket_name=str(line[3])

array_size=str(line[4])

SHOTGUN_TYPE=str(line[5])
SHOTGUN_ENTITY_ID=str(line[6])
SHOTGUN_ENTITY_TYPE=str(line[7])
SHOTGUN_ATTRIBUTE_NAME=str(line[8])
SHOTGUN_ATTRIBUTE_VALUE=str(line[9])

PIXIT_PROJECT_TYPE=str(line[10])
PIXIT_TYPE=str(line[11])
PIXIT_DELIVERY_ID=str(line[12])
PIXIT_MANIFEST_PATH=str(line[13])

print(line)


def copy_to_vfx_vendor_test(source_bucket_key, destination_bucket_key, source_bucket_name, destination_bucket_name):
    """
    :param bucket_key:
    :param source_bucket_name:
    :param destination_bucket_name:
    :return:
    """
    try:
        s3_resource = session.resource('s3')
        copy_source = {
                'Bucket': source_bucket_name,
                'Key': source_bucket_key
            }
        bucket = s3_resource.Bucket(destination_bucket_name)
        obj = bucket.Object(destination_bucket_key)
        print "Copying key %s" % source_bucket_key
        obj.copy(copy_source)
        print "Copy Completed!"
    except Exception as e:
        raise ValueError('Error while copying S3 objects %s from %s to %s - %s '%(source_bucket_key,source_bucket_name,destination_bucket_name,destination_bucket_key))
    finally:
        logger.info('Copying process ended')


def send_message_to_sns(topic_arn, message_body, message_attrs):
    """
    :param topic_arn:
    :param message_body:
    :param message_attrs:
    :return:
    """
    session = get_aws_session(region_name='ap-southeast-2', )
    sns = session.client('sns')
    response = sns.publish(TopicArn=topic_arn,
                           Message=message_body,
                           MessageAttributes=message_attrs
                           )
    return response

def main():
    """
    :return:
    """
    copy_to_vfx_vendor_test(source_bucket_key, destination_bucket_key, source_bucket_name, destination_bucket_name)
    if count == array_size:

                sleep(150);

                msg_attr={}
                msg_body = 'Changing Delivery Status to Delivered'
                msg_attr['Type'] = {"DataType": "String", "StringValue": SHOTGUN_TYPE}
                msg_attr['entityId'] = {"DataType": "Number", "StringValue": SHOTGUN_ENTITY_ID}
                msg_attr['entityType'] = {"DataType": "String", "StringValue": SHOTGUN_ENTITY_TYPE}
                msg_attr['attributeName'] = {"DataType": "String", "StringValue": SHOTGUN_ATTRIBUTE_NAME}
                msg_attr['attributeValue'] = {"DataType": "String", "StringValue": SHOTGUN_ATTRIBUTE_VALUE}
                response = send_message_to_sns(topic_arn=UAP_SNS_TOPIC, message_body=msg_body, message_attrs=msg_attr)
                print(response)

                sleep(150);

                msg_attr={}
                msg_body = 'Changing Delivery Status to Delivered'
                msg_attr['Type'] = {"DataType": "String", "StringValue": PIXIT_PROJECT_TYPE}
                msg_attr['entityId'] = {"DataType": "Number", "StringValue": PIXIT_TYPE}
                msg_attr['entityType'] = {"DataType": "String", "StringValue": PIXIT_DELIVERY_ID}
                msg_attr['attributeName'] = {"DataType": "String", "StringValue": PIXIT_MANIFEST_PATH}


if __name__ == '__main__':
    main()
