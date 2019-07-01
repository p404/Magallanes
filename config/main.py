import argparse
import configparser

def init():
    parser = argparse.ArgumentParser(description='Magallanes, nginx dynamic configuration Ingresses on a budget for Baremetal kubernetes deployments')
    parser.add_argument('-c','--config_path', help='Loads configuration', required=True)
    args = vars(parser.parse_args())
    if args['config_path']:
        return args['config_path']

config = configparser.ConfigParser()
config.read(init())

AWS_ACCESS_KEY   = config.get('route53', 'aws_access_key_id')
AWS_SECRET_KEY   = config.get('route53', 'aws_secret_access_key')
ROUTE53_REGION   = config.get('route53', 'region')
HOST_ZONE_ID     = config.get('route53', 'hosted_zone_id')
REFRESH_INTERVAL = config.get('route53', 'refresh_interval')
CNAME_HOST       = config.get('route53', 'cname')