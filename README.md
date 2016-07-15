# lambda-ec2-snap
This CloudFormation Template creates a Lambda functions that will Suspend AutoScaling and/or enable Termination Protection.

# Usage
To use this correctly, Auto-Scaling Groups and the instances that are controlled by them, should be tagged with a 'Scaling' tag and the value for this can be True or False. The template features can be set to True/False, meaning that if True, the Lambdas will search for all AutoScaling Groups (ASGs) with the Scaling Tag and any that it finds will be suspended. If the feature is set to false, the Lambdas will still run on the CloudWatch Event Schedule, however they will exit with nothing to do.

# Logic
