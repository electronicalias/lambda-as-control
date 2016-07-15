# lambda-ec2-snap
This CloudFormation Template creates Lambda functions that will Suspend AutoScaling and/or enable Termination Protection. I have found this to be useful in the phased approach of a lift and shift, where instances are not 'Cloud Ready' and therefore cannot make use of AS. 

Instead of instantiating instances without being wrapped aruond AS, we still use AS/Luanch Configs, but turn off the feature until the instances are ready to scale.

# Dependencies

1. Auto-Scaling Groups must have a "Scaling" tag, with a value of True or False
2. The scripts in the script directory need to be zipped into a zip file, the name for which is used in the parameter S3Key

# Logic

1. After uploading the FILE.zip file to S3 to the bucket you choose, with the key you choose, run the cloudformation template
2. Choose True/False to enable/disable the feature
3. Set the "Scaling" tag appropriately:

  True: Resume Auto Scaling Actions (all) and Turn OFF Termination Protection on the instances provisioned by that ASG
  False: Suspend Auto Scaling Actions for any Instances that have the tag "Scaling" = "False"
  
Note: Remember the tags on instances belonging to ASGs are set by the ASG tags if you have "ProvisionAtLaunch":"True"

Note: Any instances or ASGs that do not have the "Scaling" tag, are put into an 'Other' List and nothing is changed about their state.
