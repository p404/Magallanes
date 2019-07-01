from common.utils import logger
from route53.api import add_dns_record, delete_dns_record
from storage.api import add_host_consul, delete_host_consul

def add_host(hostname, host, external, port):
    add_host_consul(hostname, host, external, port)
    add_dns_record(hostname, host, external)
    message = "Added new host {}".format(hostname)
    logger('info', message)

def delete_host(hostname, host, external, port):
    delete_host_consul(hostname)
    delete_dns_record(hostname, host, external)
    message = "Deleted host {}".format(hostname)
    logger('info', message)
