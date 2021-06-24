"""
The command line interface to stackility.

Major help from: https://www.youtube.com/watch?v=kNke39OZ2k0
"""
import os
import sys
import boto3
import logging
import click
import sys
import platform

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='[%(levelname)s] %(asctime)s (%(module)s) %(message)s',
    datefmt='%Y/%m/%d-%H:%M:%S'
)

from lookup.utility import init_boto3_clients
logger = logging.getLogger(__name__)
DEFAULT_REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

services = [
    'ssm'
]

valid_systems = [
    'linux',
    'darwin'
]


@click.group()
@click.version_option(version='0.1.0')
def cli():
    pass


@cli.command()
@click.option('--key', '-k', help='SSM key to extract', required=True)
@click.option('--profile', '-p', help='AWS profile')
@click.option('--region', '-r', help='AWS region')
def ssm(key, profile, region):
    try:
        if region is None:
            region = DEFAULT_REGION

        clients = init_boto3_clients(services, profile=profile, region=region)
        ssm_client = clients['ssm']
        response = ssm_client.get_parameter(Name=key, WithDecryption=True)
        wrk = response.get('Parameter', {}).get('Value', None)
        if wrk:
            print(wrk, end='')
        else:
            logger.info(f'no value found for {key=}')
    except Exception as wtf:
        logger.error(wtf, exc_info=False)
        sys.exit(1)


def find_myself():
    s = boto3.session.Session()
    region = s.region_name
    if region:
        return region
    else:
        return 'us-east-1'


def verify_real_system():
    try:
        current_system = platform.system().lower()
        return current_system in valid_systems
    except:
        return False


if not verify_real_system():
    print('error: unsupported system')
    sys.exit(1)
