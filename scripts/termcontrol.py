import boto3
import logging
import collections

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):

    fstate = event['FeatureState']
    
    if 'False' in fstate:
        print "Nothing to do, function disabled."
    else:
        rname = event['Region']
        action = collections.defaultdict(list)
        ec2 = boto3.client('ec2', rname)
        ec2res = boto3.resource('ec2', rname)
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
                action['Other'].append(instance['InstanceId'])

        print "Instances missing tags: %s" % (
            action['Other'])
        print "Instances being Protected: %s" % (
            action['False'])
        print "Instances with Protection Off: %s" % (
            action['True'])

        for enableprotection in action['False']:
            instance = ec2res.Instance(enableprotection)
            response = instance.modify_attribute(
                DisableApiTermination={
                    'Value': True
                },
            )
            print "Termination Protection has been Enabled for: %s" % (i['InstanceId'])

        for disableprotection in action['True']:
            instance = ec2res.Instance(disableprotection)
            response = instance.modify_attribute(
                DisableApiTermination={
                    'Value': False
                },
            )
            print "Termination Protection has been Disabled for: %s" % (i['InstanceId'])