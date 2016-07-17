# lambda-ec2-snap
This tool pertains to a solution in Amazon Web Services (AWS) that will disable AutoScaling (AS) and enable Termination Protection (TS). I have found this to be useful in a phased approach to lift and shift migrations, where instances are not 'Cloud Ready' and therefore cannot make use of AS. But, instead of instantiating instances without being wrapped up by AS, we still use AS/Luanch Configurations (LC), but turn off the features until the instances are ready to scale.

# Dependencies

1. Auto-Scaling Groups must have a "Scaling" tag, with a value of True or False
2. The scripts in the script directory need to be zipped into a zipfile, the name for which is used in the parameter S3Key
3. The zipfile needs to be hosted in an S3 Bucket

# Logic

1. After uploading the FILE.zip file to S3 to the bucket you choose, with the key you choose, run the CloudFormation (CFN) template
2. Choose True/False to enable/disable the feature when the CFN template is run
3. Set the "Scaling" tag appropriately:

  True: Resume Auto Scaling Actions (all) and Turn OFF Termination Protection on the instances provisioned by that ASG
  False: Suspend Auto Scaling Actions for any Instances that have the tag "Scaling" = "False"
  
Note: Remember the tags on instances belonging to ASGs are set by the ASG tags if you have "ProvisionAtLaunch":"True"

Note: Any instances or ASGs that do not have the "Scaling" tag, are put into an 'Other' List and nothing is changed about their state.
