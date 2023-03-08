Before Running:
    run:
        az-login
    check:
        if both azure and gcp sdk's are setup and logged in
    
    
    Required Libraries:
        import os
        import subprocess
        import configparser
        from subprocess import PIPE, run
        from datetime import datetime

    This program will automatically parse .conf files are create the VM's described inside them. It will then create the output file and rename the .conf
    files. The program will the prompt users asking them if they want to open any ports. Follow the prompts to open ports.







