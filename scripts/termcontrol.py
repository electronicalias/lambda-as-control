import boto3
import logging

logging.getLogger().setLevel(logging.DEBUG)


def lambda_handler(event, context):

    fstate = event['FeatureState']
    
    if 'False' in fstate:
        print "Nothing to do, function disabled."
    else:
        rname = event['Region']
        ec2 = boto3.client('ec2', rname)
        reservations = ec2.describe_instances(
            Filters=[
                {'Name': 'tag-key', 'Values': ['Scaling']},
                {'Name': 'tag-value', 'Values': [fstate]},
            ])['Reservations']
        
        instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], [])

        for instance in instances:

            instance = ec2.Instance(i['InstanceId'])
            response = instance.modify_attribute(
                DisableApiTermination={
                    'Value': True
                },
            )
            print "Termination Protection has been Enabled for: %s" % (i['InstanceId'])