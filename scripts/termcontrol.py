import boto3
import logging

logging.getLogger().setLevel(logging.DEBUG)


def lambda_handler(event, context):

    fstate = event['FeatureState']
    
    if 'False' in fstate:
        print "Nothing to do, function disabled."
    else:
        rname = event['Region']
        action = collections.defaultdict(list)
        ec2 = boto3.client('ec2', rname)
        reservations = ec2.describe_instances(
            Filters=[
                {'Name': 'tag-key', 'Values': ['Scaling']},
            ])['Reservations']

        instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], [])

        for instance in instances:
            try:
                value = [
                    str(val.get('Value')) for val in instance['Tags']
                    if val['Key'] == 'Scaling'][0]
                action[value].append(instance['InstanceId'])
            except:
                action['other'].append(instance['InstanceId'])

            for enableprotection in action['False']:
                instance = ec2.Instance(enableprotection)
                    response = instance.modify_attribute(
                        DisableApiTermination={
                            'Value': True
                        },
                    )
                    print "Termination Protection has been Enabled for: %s" % (i['InstanceId'])

            for disableprotection in action['True']:
                instance = ec2.Instance(disableprotection)
                    response = instance.modify_attribute(
                        DisableApiTermination={
                            'Value': False
                        },
                    )
                    print "Termination Protection has been Disabled for: %s" % (i['InstanceId'])