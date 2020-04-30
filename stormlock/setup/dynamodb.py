#!/usr/bin/env python3

from typing import Optional

import boto3


def create_lock_table(
        table_name: str = 'stormlock',
        endpoint: Optional[str] = None,
        billing_mode: str = 'PAY_PER_REQUEST',
        read_capacity: Optional[int] = None,
        write_capacity: Optional[int] = None,
        sse: Optional[str] = None,
        sse_key_id: Optional[str] = None,
        tags: dict = {},
        region: Optional[str] = None,
        profile: Optional[str] = None,
        ):
    session = boto3.session.Session(region_name=region, profile_name=profile)
    client = session.client('dynamodb', endpoint_url=endpoint)

    config_args = {}
    if billing_mode != 'PAY_PER_REQUEST':
        config_args['ProvisionedThroughput'] = {
                'ReadCapacityUnits': read_capacity,
                'WriteCapacityUnits': write_capacity,
                }
    if sse:
        config_args['SSESpecification'] = {
                'Enabled': True,
                'SSEType': sse,
                'KMSMasterKeyId': sse_key_id,
                }

    client.create_table(
            TableName=table_name,
            KeySchema=[{
                'AttributeName': 'resource',
                'KeyType': 'HASH'
                }],
            AttributeDefinitions=[{
                'AttributeName': 'resource',
                'AttributeType': 'S'
            }],
            BillingMode=billing_mode,
            Tags=[{'Key': k, 'Value': v} for (k, v) in tags.items()],
            **config_args)
    # client.get_waiter('table_exists').wait(TableName=table_name)
    client.update_time_to_live(
            TableName=table_name,
            TimeToLiveSpecification={
                'Enabled': True,
                'AttributeName': 'expires',
                })

# TODO: add a main method that parses CLI flags
