import boto3
from common.utils import hash
from config.main  import (AWS_ACCESS_KEY, AWS_SECRET_KEY, ROUTE53_REGION,
                          HOST_ZONE_ID, REFRESH_INTERVAL, CNAME_HOST)

def record_type(external):
    return "CNAME" if external is True else "A"

def host_value(host, record_type):
    return CNAME_HOST if record_type == 'CNAME' else host

def route53_client():
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    return session.client('route53')

def add_dns_record(hostname, host, external, client=route53_client()):
    delete_current_dns_record(hostname)
    client.change_resource_record_sets(
        HostedZoneId= HOST_ZONE_ID,
        ChangeBatch={
            "Comment": "Added by Magallanes",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": hostname,
                        "SetIdentifier": hash(hostname),
                        "Region": ROUTE53_REGION,
                        "Type": record_type(external),
                        "TTL": int(REFRESH_INTERVAL),
                        "ResourceRecords": [
                            {
                                "Value": host_value(host, record_type(external))
                            },
                        ],
                    }
                },
            ]
        }
    )

def delete_dns_record(hostname, host, external, client=route53_client()):
    client.change_resource_record_sets(
        HostedZoneId= HOST_ZONE_ID,
        ChangeBatch={
            "Comment": "Deleted by Magallanes",
            "Changes": [
                {
                    "Action": "DELETE",
                    "ResourceRecordSet": {
                        "Name": hostname,
                        "SetIdentifier": hash(hostname),
                        "Region": ROUTE53_REGION,
                        "Type": record_type(external),
                        "TTL": int(REFRESH_INTERVAL),
                        "ResourceRecords": [
                            {
                                "Value": host_value(host, record_type(external))
                            },
                        ],
                    }
                },
            ]
        }
    )

def delete_current_dns_record(hostname, client=route53_client()):
    paginator = client.get_paginator('list_resource_record_sets')
    source_zone_records = paginator.paginate(HostedZoneId=HOST_ZONE_ID)
    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if 'SetIdentifier' in record:
                if record['SetIdentifier'] == hash(hostname):
                    hostname    = record['Name'].rstrip('.')
                    record_type = record['Type']
                    host_value  = record['ResourceRecords'][0]['Value']
                    ttl         = record['TTL']
                    client.change_resource_record_sets(
                        HostedZoneId= HOST_ZONE_ID,
                        ChangeBatch={
                            "Comment": "Deleted by Magallanes",
                            "Changes": [
                                {
                                    "Action": "DELETE",
                                    "ResourceRecordSet": {
                                        "Name": hostname,
                                        "SetIdentifier": hash(hostname),
                                        "Region": ROUTE53_REGION,
                                        "Type": record_type,
                                        "TTL": ttl,
                                        "ResourceRecords": [
                                            {
                                                "Value": host_value
                                            },
                                        ],
                                    }
                                },
                            ]
                        }
                    )