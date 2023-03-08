import boto3
from boto3.dynamodb.conditions import Key, Attr
import csv
import json
import sys








def addToCountry(dynamodb, iso3, lang) :
    table = dynamodb.Table('gnodwell_country_data')
    try:
        item = getItemFromCountry(dynamodb, 'gnodwell_country_data', iso3)
        if (item == -1) :
            print("Unable to find entry")
        else :
            if (item.get('Language 1') == '') :
                table.update_item(
                        Key={'ISO3': iso3},
                        ExpressionAttributeNames = {
                                '#lang': 'Language 1'
                                },
                        UpdateExpression="set #lang = :newLang",
                        ExpressionAttributeValues= {
                                ':newLang': lang
                                }
                    )
            elif (item.get('Language 2') == '') :
                table.update_item(
                        Key={'ISO3': iso3},
                        ExpressionAttributeNames = {
                                '#lang': 'Language 2'
                                },
                        UpdateExpression="set #lang = :newLang",
                        ExpressionAttributeValues= {
                                ':newLang': lang
                                }
                    )
            elif (item.get('Language 3') == '') :
                table.update_item(
                        Key={'ISO3': iso3},
                        ExpressionAttributeNames = {
                                '#lang': 'Language 3'
                                },
                        UpdateExpression="set #lang = :newLang",
                        ExpressionAttributeValues= {
                                ':newLang': lang
                                }
                    )
            else :
                print("Unable to add language")
    except Exception as e:
        print(e)



def getItemFromCountry(dynamodb, table_name, iso3) :
    try :
        table = dynamodb.Table(table_name)
        response = table.query(
                KeyConditionExpression=Key('ISO3').eq(iso3)
                )
        item = response['Items']
        return item[0]

    except Exception as e:
        print(e)

    return -1


def addToPopulation(dynamodb, year, country, population) :
    table = dynamodb.Table('gnodwell_population_data')
    item = getItemFromPopulation(dynamodb, year, country)

    if (item == -1) :
        print("Unable to add population")
    else :
        try :
            table.update_item(
                    Key={'Country': country,
                        'Year': year
                        },
                    ExpressionAttributeNames = {
                            '#pop': 'Population'
                            },
                    UpdateExpression="set #pop = :newPop",
                    ExpressionAttributeValues= {
                            ':newPop': population
                            }
                )

        except Exception as e:
            print(e)



def getItemFromPopulation(dynamodb, year, country) :
    try :
        table = dynamodb.Table('gnodwell_population_data')
        response = table.query(
                KeyConditionExpression=Key('Country').eq(country)
                )
        item = response['Items']
        #print(item)
        for x in item:
            if (x.get('Population') == '') :
                return x
                print (x)

    except Exception as e:
        print(e)
        return -1


    return -1




#main
fp = open('credentials', 'r')


lines = fp.readlines()

for x in lines:
    hold = x.split(' ')
    if (hold[0] == 'aws_access_key_id') :
        access_key = hold[2].strip('\n')
    elif (hold[0] == 'aws_secret_access_key') :
        secret_access = hold[2].strip('\n')



session = boto3.Session(region_name='ca-central-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access)
dynamodb = session.resource('dynamodb', region_name='ca-central-1')


while (True):
    dataType = input("What table would you like to add to ('country_data', 'population_data', 'quit'): ")
    dataType = dataType.strip()
    if (dataType == 'country_data') :
        iso3 = input("ISO3 code: ")
        iso3 = iso3.strip()
        iso3 = iso3.upper()
        lang = input("Language: ")
        lang = lang.strip()
        addToCountry(dynamodb, iso3, lang)
    elif (dataType == 'population_data') :
        year = input("Year: ")
        country = input("Country: ")
        population = input("Population: ")

        year = year.strip()
        country = country.strip()
        population = population.strip()

        addToPopulation(dynamodb, year, country, population)
    elif(dataType == 'quit') :
        exit(0)
    else :
        print('Incorrect User Input')
