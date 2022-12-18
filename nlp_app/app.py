import json
import os
import time
from nltk.corpus import wordnet as wn
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_synonyms(text):
    text = text.replace(" ", "_")
    terms = text.split(",")
    synonyms = []
    for term in terms:
        synonym_list = wn.synsets(term)
    for synonym in synonym_list:
        synonyms.append(synonym.lemmas()[0].name())
    return synonyms


def lambda_handler(event, context):
    print("Lambda function ARN:", context.invoked_function_arn)
    print("CloudWatch log stream name:", context.log_stream_name)
    print("CloudWatch log group name:", context.log_group_name)
    print("Lambda Request ID:", context.aws_request_id)
    print("Lambda function memory limits in MB:", context.memory_limit_in_mb)

    logger.info('## ENVIRONMENT VARIABLES')
    logger.info(os.environ)
    logger.info('## EVENT')
    logger.info(event)

    keywords = event['queryStringParameters']['keywords']

    # We have added a 1 second delay so you can see the time remaining in get_remaining_time_in_millis.
    time.sleep(1)
    print("Lambda time remaining in MS:", context.get_remaining_time_in_millis())

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "related_keywords": get_synonyms(keywords)
        }),
    }

    return response

# Sample pure Lambda function Parameters ---------- event: dict, required API Gateway Lambda Proxy Input Format Event
# doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway
# -simple-proxy-for-lambda-input-format context: object, required Lambda Context runtime methods and attributes
# Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html Returns ------ API Gateway
# Lambda Proxy Output Format: dict
#
#     Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html


# try:
#     ip = requests.get("http://checkip.amazonaws.com/")
# except requests.RequestException as e:
#     # Send some context about this error to Lambda Logs
#     print(e)

#     raise e
