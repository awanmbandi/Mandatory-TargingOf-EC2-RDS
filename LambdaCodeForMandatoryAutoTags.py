import json
import boto3

def create_elb_default_tags(elb_client,elb_names,tag):
    for elb_name in elb_names:
        elb_response = elb_client.add_tags(
            LoadBalancerNames=[elb_name],
            Tags=[
            {
                'Key': 'BarometerIT',
                'Value': '041800001DQ5'
            },
            {
                'Key': 'costcenter',
                'Value': '6590101400'
            },
            {
                'Key': 'Application',
                'Value': 'Pharmacy'
            },
            {
                'Key': 'Owner Department',
                'Value': 'IRxIT'
            },
            {
                'Key': 'ResourceType',
                'Value': "Compute"
            },
            {
                'Key': 'Environment',
                'Value': 'Dev'
            }
        ]
        )
        print(elb_response)
        if elb_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Tags Created Successfully")

def create_elbv2_default_tags(elbv2_client,elbv2_arns,tag):
    for elbv2_arn in elbv2_arns:
        elbv2_response = elbv2_client.add_tags(
            ResourceArns=[elbv2_arn],
            Tags=[
            {
                'Key': 'BarometerIT',
                'Value': '041800001DQ5'
            },
            {
                'Key': 'costcenter',
                'Value': '6590101400'
            },
            {
                'Key': 'Application',
                'Value': 'Pharmacy'
            },
            {
                'Key': 'Owner Department',
                'Value': 'IRxIT'
            },
            {
                'Key': 'ResourceType',
                'Value': "Compute"
            },
            {
                'Key': 'Environment',
                'Value': 'Dev'
            }
        ]
        )
        print(elbv2_response)
        if elbv2_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Tags Created Successfully")

def create_ecs_default_tags(ecs_client,ecs_arns,tag):
    for ecs_arn in ecs_arns:
        ecs_response = ecs_client.tag_resource(
            resourceArn=ecs_arn,
            tags=[
            {
                'key': 'BarometerIT',
                'value': '041800001DQ5'
            },
            {
                'key': 'costcenter',
                'value': '6590101400'
            },
            {
                'key': 'Application',
                'value': 'Pharmacy'
            },
            {
                'key': 'Owner Department',
                'value': 'IRxIT'
            },
            {
                'key': 'ResourceType',
                'value': "Compute"
            },
            {
                'key': 'Environment',
                'value': 'Dev'
            }
        ]
        )
        print(ecs_response)
        if ecs_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Tags Created Successfully")

def create_efs_default_tags(efs_client,efs_ids,tag):
    for efs_id in efs_ids:
        efs_response = efs_client.create_tags(
            FileSystemId=efs_id,
            Tags=[
            {
                'Key': 'BarometerIT',
                'Value': '041800001DQ5'
            },
            {
                'Key': 'costcenter',
                'Value': '6590101400'
            },
            {
                'Key': 'Application',
                'Value': 'Pharmacy'
            },
            {
                'Key': 'Owner Department',
                'Value': 'IRxIT'
            },
            {
                'Key': 'ResourceType',
                'Value': "Compute"
            },
            {
                'Key': 'Environment',
                'Value': 'Dev'
            }
        ]
        )
        if efs_response['ResponseMetadata']['HTTPStatusCode'] == 204:
            print("Tags Created Successfully")


def create_default_tags(ec2_client,ids,tag):
    response = ec2_client.create_tags(
            Resources=ids,
            Tags=[
            {
                'Key': 'BarometerIT',
                'Value': '041800001DQ5'
            },
            {
                'Key': 'costcenter',
                'Value': '6590101400'
            },
            {
                'Key': 'Application',
                'Value': 'Pharmacy'
            },
            {
                'Key': 'Owner Department',
                'Value': 'IRxIT'
            },
            {
                'Key': 'ResourceType',
                'Value': "Compute"
            },
            {
                'Key': 'Environment',
                'Value': 'Dev'
            }
        ]
        )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Tags Created Successfully")

def lambda_handler(event, context):
    # TODO implement
    ec2_ids = []
    ec2_root_ebs_ids=[]
    ebs_ids = []
    sg_ids = []
    efs_ids = []
    ecs_arns = []
    elb_names = []
    elbv2_arns = []
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')
    efs_client = boto3.client('efs')
    ecs_client = boto3.client('ecs')
    elb_client = boto3.client('elb')
    elbv2_client = boto3.client('elbv2')
    detail = event['detail']
    print(detail)
    print(event)
    eventname = detail['eventName']

    if eventname == 'RunInstances':
        print(eventname)
        items = detail['responseElements']['instancesSet']['items']
        for item in items:
            ec2_ids.append(item['instanceId'])

            instance = ec2_resource.Instance(str(item['instanceId']))
            ec2_volumes = instance.volumes.all()
            for vol in ec2_volumes:
                ec2_root_ebs_ids.append(vol.id)

        create_default_tags(ec2_client, ec2_ids, "SVR")
        create_default_tags(ec2_client, ec2_root_ebs_ids, "EBS")

    if eventname == 'CreateVolume':
        print(eventname)
        ebs_ids.append(detail['responseElements']['volumeId'])
        create_default_tags(ec2_client, ebs_ids, "EBS")

    if eventname == 'CreateSecurityGroup':
        print(eventname)
        sg_ids.append(detail['responseElements']['groupId'])
        create_default_tags(ec2_client, sg_ids, "GRP")

    if eventname == 'CreateFileSystem':
        print(eventname)
        efs_ids.append(detail['responseElements']['fileSystemId'])
        create_efs_default_tags(efs_client, efs_ids, "EFS")

    if eventname == 'CreateCluster':
        print(eventname)
        ecs_arns.append(detail['responseElements']['cluster']['clusterArn'])
        create_ecs_default_tags(ecs_client, ecs_arns, "ECS")

    if eventname == 'CreateLoadBalancer':
        print(eventname)
        if "loadBalancers" in str(detail):
            elbv2_arns.append(detail['responseElements']['loadBalancers'][0]['loadBalancerArn'])
            create_elbv2_default_tags(elbv2_client, elbv2_arns, "ELB")
        else:
            elb_names.append(detail['requestParameters']['loadBalancerName'])
            create_elb_default_tags(elb_client, elb_names, "ELB")
