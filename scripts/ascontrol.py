import boto3
import logging
import collections

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):

    fstate = event['FeatureState']
    
    if 'False' in fstate:
        print "Nothing to do, AutoScaling feature not enabled."
    elif 'True' in fstate:
        rname = event['Region']
        action = collections.defaultdict(list)
        asc = boto3.client('autoscaling',rname)
        asgroups = asc.describe_auto_scaling_groups(
            )['AutoScalingGroups']

        for group in asgroups:
            try:
                state = [
                    str(val.get('Value')) for val in group['Tags']
                    if val['Key'] == 'Scaling'][0]
                action[state].append(group['AutoScalingGroupName'])
            except:
                action['Other'].append(group['AutoScalingGroupName'])
        
        print "Groups missing tags: %s" % (
            action['Other'])
        print "Groups being disalbed: %s" % (
            action['False'])
        print "Groups being enabled: %s" % (
            action['True'])

        for disabledasg in action['False']:
            asc.suspend_processes(
                AutoScalingGroupName=disabledasg,
                ScalingProcesses=[
                    'Terminate',
                    'ReplaceUnhealthy',
                    'AZRebalance',
                    'ScheduledActions',
                    'Launch',
                    'HealthCheck',
                    'AlarmNotification',
                    'AddToLoadBalancer'
                ]
            )
            print "Disabled Auto Scaling for: %s" % (
                disabledasg)

        for enabledasg in action['True']:
            asc.resume_processes(
                AutoScalingGroupName=enabledasg,
                ScalingProcesses=[
                    'Terminate',
                    'ReplaceUnhealthy',
                    'AZRebalance',
                    'ScheduledActions',
                    'Launch',
                    'HealthCheck',
                    'AlarmNotification',
                    'AddToLoadBalancer'
                ]
            )
            print "Enabled Auto Scaling for: %s" % (
                enabledasg)