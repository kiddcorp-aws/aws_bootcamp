# Backup all in-use volumes in NV region

import boto3

def lambda_handler(event, context):

        # Connect to N. Virginia region
        ec2 = boto3.client('ec2', "us-east-1")
    
        # Get all in-use volumes in all regions  
        result = ec2.describe_volumes( Filters=[{'Name': 'status', 'Values': ['in-use']}])
        
        for volume in result['Volumes']:
            print ("Backing up %s in %s" % (volume['VolumeId'], volume['AvailabilityZone']))
        
            # Create snapshot
            result = ec2.create_snapshot(VolumeId=volume['VolumeId'],Description='Created by Lambda backup function ebs-snapshots')
        
            # Get snapshot resource 
            ec2resource = boto3.resource('ec2', "us-east-1")
            snapshot = ec2resource.Snapshot(result['SnapshotId'])
        
            volumename = 'N/A'
        
            # Find name tag for volume if it exists
            if 'Tags' in volume:
                for tags in volume['Tags']:
                    if tags["Key"] == 'Name':
                        volumename = tags["Value"]
        
            # Add volume name to snapshot for easier identification
            snapshot.create_tags(Tags=[{'Key': 'Name','Value': volumename}])