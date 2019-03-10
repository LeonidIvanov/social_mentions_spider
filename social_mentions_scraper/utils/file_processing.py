import os

import boto3

from social_mentions_scraper.settings import BUCKET_NAME


def send_file_to_aws(filename):
    if BUCKET_NAME:
        client = boto3.client('s3')
        client.upload_file(filename, BUCKET_NAME, filename)
    else:
        print("Add BUCKET_NAME to settings to store results in AWS bucket")


def delete_file(filename):
    os.remove(filename)
