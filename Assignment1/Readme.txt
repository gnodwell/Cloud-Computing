How to run :
    Ensure that the S5-S3conf file is set up properly (I have my credentials in there already)
    type python3 aws-shell.py to start the shell

Normal Behaviour of my Shell:
    The Shell will prompt S5>
    This is where you type your commands
    I have implemented all of the required commands
    A limitation is ''list -l', I did not complete the long for so this command will print the same as 'list'
    If the commands are run properly there should be no problems
    I did not do extensive testing so inputting improper command formats may have unexpected outcomes

Required Files :
    aws-shell.py
    S5-S3conf

    

Required Libraries:
    os
    sys
    boto3
    subprocess
    json

Testing
    this has only been tested on MacOs, should be fine as all dependenices are python based
