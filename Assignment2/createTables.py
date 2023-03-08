import boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import json
import sys






def createTable(dynamodb, table_name) :
    if (table_name == 'gnodwell_country_data') :
        try :
            table = dynamodb.create_table (
                TableName = 'gnodwell_country_data',
                KeySchema=[
                    {
                        'AttributeName': 'ISO3',
                        'KeyType': 'HASH'

                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'ISO3',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits' : 10,
                    'WriteCapacityUnits': 10
                }
            )

            table.wait_until_exists()
            print('gnodwell_country_data created')
            return 0
        except Exception as e :
            return -1

    elif (table_name == 'gnodwell_population_data'):
        try :
            table = dynamodb.create_table (
                TableName = 'gnodwell_population_data',
                KeySchema=[
                    {
                        'AttributeName': 'Country',
                        'KeyType': 'HASH'

                    },
                    {
                        'AttributeName': 'Year',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Country',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'Year',
                        'AttributeType': 'S'
                    }

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits' : 10,
                    'WriteCapacityUnits': 10
                }
            )

            table.wait_until_exists()
            print('gnodwell_population_data created')
            return 0
        except Exception as e :
            return -1

    elif (table_name == 'gnodwell_gdp_data') :
        try :
            table = dynamodb.create_table (
                TableName = 'gnodwell_gdp_data',
                KeySchema=[
                    {
                        'AttributeName': 'Country',
                        'KeyType': 'HASH'

                    },
                    {
                        'AttributeName': 'Year',
                        'KeyType': 'RANGE'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'Country',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'Year',
                        'AttributeType': 'S'
                    }

                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits' : 10,
                    'WriteCapacityUnits': 10
                }
            )

            table.wait_until_exists()
            print('gnodwell_gdp_data created')
            return 0
        except Exception as e :
            return -1

    else :
        print("Cannot Create Table")



def deleteTable(client, table_name):
    try :
        client.delete_table(TableName=table_name)
        print("Deleted ", table_name)
        return 0
    except Exception as e:
        print("Unable to delete table")
        print(e)
        return -1



def addItem(dynamodb, table_name, item) :
    try :
        table = dynamodb.Table(table_name)
        itemTBA = table.put_item(Item=item)
        return 0
    except Exception as e:
        print ("Unable to add item")
        print (e)
        return -1



def loadCountryData(dynamodb) :
    path = './tables/' + 'shortlist_capitals.csv'
    with open(path, 'r') as file:
        x = file.readlines()

    path = './tables/' + 'shortlist_area.csv'
    with open(path, 'r') as file:
        y = file.readlines()

    path = './tables/' + 'shortlist_languages.csv'
    with open(path, 'r') as file:
        z = file.readlines()

    i = 0
    for j in x:
        capitals = x[i].split(',')
        my_country = capitals[1]
        for check in y :
            hold = check.split(',')
            if (hold[1] == my_country) :
                areas = hold
        for check in z :
            hold = check.split(',')
            if (hold[1] == my_country) :
                languages = hold

        length = len(languages) - 2
        if (i > 0) :
            if (length == 1):
                item = {
                        'ISO3': capitals[0],
                        'Country': capitals[1],
                        'Capital': capitals[2].strip('\n'),
                        'Area': areas[2].strip('\n'),
                        'Language 1': languages[2].strip('\n'),
                        'Language 2': '',
                        'Language 3': ''
                       }
            elif (length == 2) :
                item = {
                        'ISO3': capitals[0],
                        'Country': capitals[1],
                        'Capital': capitals[2].strip('\n'),
                        'Area': areas[2].strip('\n'),
                        'Language 1': languages[2],
                        'Language 2': languages[3].strip('\n'),
                        'Language 3': ''
                       }
            elif (length == 3) :
                item = {
                        'ISO3': capitals[0],
                        'Country': capitals[1],
                        'Capital': capitals[2].strip('\n'),
                        'Area': areas[2].strip('\n'),
                        'Language 1': languages[2],
                        'Language 2': languages[3],
                        'Language 3': languages[4].strip('\n')
                       }
            addItem(dynamodb, 'gnodwell_country_data', item)

        i = i+1
    print("Loaded gnodwell_country_data")
    return 0



def loadPopulationData(dynamodb):
    path = './tables/shortlist_curpop.csv'
    i = 0
    with open(path) as file:
        reader = csv.reader(file)
        for row in reader:
            if (i > 0):
                for x in range(50):
                    year = 1970
                    #print(row[x])
                    item = {
                            'Country':row[0],
                            'Year': str(x+1970),
                            'Population': row[x+2]
                            }
                    #print(item)
                    addItem(dynamodb, 'gnodwell_population_data', item)
            i = 1
    print("Loaded gnodwell_population_data")
    return 0



def loadGDPData(dynamodb) :
    path = './tables/' + 'shortlist_gdppc.csv'
    with open(path, 'r') as file:
        x = file.readlines()

    path = './tables/' + 'shortlist_curpop.csv'
    with open(path, 'r') as file:
        y = file.readlines()


    i = 0
    year = 1970
    for z in x:
        if (i > 0) :
            gdppc = x[i].split(',')
            pop = y[i].split(',')
            currency = pop[1]
            country = gdppc[0]
            for j in range(1,51):
                item = {
                        'Country': country,
                        'Year': str(year+j-1),
                        'Currency': currency,
                        'gdppc': gdppc[j].strip('\n')
                        }
                addItem(dynamodb, 'gnodwell_gdp_data', item)
        i = i + 1

    print("Loaded gnodwell_gdp_data")
    return 0



def deleteItem(dynamodb, table_name, key) :
    try:
        table = dynamodb.Table(table_name)
        response = table.delete_item(
                Key=key
                )
        return 0
    except Exception as e:
        return -1




#main
fp = open("credentials", "r")

lines = fp.readlines()
for x in lines :
    hold = x.split(" ")
    if (hold[0] == 'aws_access_key_id') :
        access_key = hold[2].strip('\n')
    elif (hold[0] == 'aws_secret_access_key') :
        secret_access = hold[2].strip('\n')




session = boto3.Session(region_name='ca-central-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access)
dynamodb = session.resource('dynamodb', region_name='ca-central-1')
client = boto3.client('dynamodb', region_name='ca-central-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access)


while (True) :
    usrInput = input("Would you like to create or delete a table ('create', 'delete', 'quit'): ")
    if (usrInput == 'create') :
        print("Please wait a minute")
        result = createTable(dynamodb, 'gnodwell_country_data')
        result = createTable(dynamodb, 'gnodwell_population_data')
        result = createTable(dynamodb, 'gnodwell_gdp_data')
        result = loadCountryData(dynamodb)
        result = loadPopulationData(dynamodb)
        result = loadGDPData(dynamodb)
    elif (usrInput == 'delete') :
        deleteTable(client, 'gnodwell_country_data')
        deleteTable(client, 'gnodwell_population_data')
        deleteTable(client, 'gnodwell_gdp_data')
    elif(usrInput == 'quit'):
        exit(0)

    else :
        print("Unexpected user inputer")









