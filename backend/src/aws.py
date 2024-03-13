import os
import sys
import uuid
import boto3
from dotenv import load_dotenv

cwd = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(cwd)

from .utils import load_yaml_file

config = load_yaml_file(file_path=os.path.join(cwd, 'backend', 'config.yaml'))
load_dotenv(os.path.join(cwd, '.env'))

os.environ['AWS_ACCESS_KEY_ID'] = os.environ['AWS_ACCESS_KEY']
os.environ['AWS_SECRET_ACCESS_KEY'] = os.environ['AWS_SECRET_KEY']


class AWSClient:
    def __init__(self, config):
        self.client = boto3.client('s3')
        self.bucket_name = config['aws']['bucket_name']

    def upload_file(self, text, filename):
        if filename != '':
            assert len(filename) != 0 and filename != ''
            response = self.client.put_object(
                                        Body=text,
                                        Bucket=self.bucket_name,
                                        Key=filename
                                    )
            if response['ResponseMetadata']['HTTPStatusCode']:
                print('File saved')
                return True, filename
            else:
                print('File not saved')
                return False, filename
        else:
            return False, filename

    def get_file(self, filename):
        response = self.client.get_object(
                                    Bucket=self.bucket_name,
                                    Key=filename
                                )
        text = response['Body'].read().decode('utf-8')
        return text
