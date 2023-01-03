import json
import os
import time
import nltk
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
    if not keywords:
        return {
            'statusCode': 400,
            'body': json.dumps('No keywords provided!')
        }

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "related_keywords": get_synonyms(keywords)
        }),
    }

    return response
