import json
import logging
import os
import nltk
from nltk.corpus import wordnet as wn

logger = logging.getLogger()
logger.setLevel(logging.INFO)

nltk.data.path.append('/tmp/nltk_data')
nltk.download('wordnet', download_dir='/tmp/nltk_data')


def get_synonyms(text):
    text = text.replace(" ", "_")
    terms = text.split(",")
    synonyms = []
    for term in terms:
        synonym_list = wn.synsets(term)
        for synonym in synonym_list:
            name = synonym.lemmas()[0].name()
            if name not in synonyms:
                synonyms.append(name)
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

    synonyms = get_synonyms(keywords)
    logger.info('## SYNONYMS')
    logger.info(synonyms)

    if not keywords:
        return {
            'statusCode': 400,
            'body': json.dumps('No keywords provided!')
        }
    if keywords:
        return {
            'statusCode': 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            'body': json.dumps({'synonyms': synonyms})
        }
