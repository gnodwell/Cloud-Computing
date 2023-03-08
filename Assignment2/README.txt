


This Consits of 3 different programs:
    createTables : Creates and deletes tables in the dynamodb database
    addInformation: Enables user to add Languages to 'gnodwell_country_data' or add a population to 'gnodwell_population_data'
    reports : Allows a user to print the Reports

To Run:
    - This program connects to aws from the file 'credentials' in the working directory which connects to my account (gnodwell)
    - If user wants to connect to their own account they must change my access keys in the credential file
    - The /tables/ contains the necessary files that will be added to the database (The createTables must have these files)
    - To start running a program type 'python3 <program_name>'
    - The program will then prompt the user to the actions they can take


Required Files:
    - shortlist_area.csv
    - shortlist_capitals.csv
    - shortlist_curpop.csv
    - shortlist_gdppc.csv
    - shortlist_languages.csv
    - credentials
    - createTables.py
    - addInformation.py
    - reports.py

Required Libraies
    - boto3
    - csv
    - json
    - sys

Testing:
    - This has been tested on my personal Mac and has had no problems
