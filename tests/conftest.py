import json
import os
import pytest


os.environ['ENV'] = 'dev'
os.environ['DEFAULT_DATA_LIMIT'] = '20'


@pytest.fixture(scope='session')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
