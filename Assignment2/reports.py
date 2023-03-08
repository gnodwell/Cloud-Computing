import boto3
from boto3.dynamodb.conditions import Key, Attr




def calcAreaRank(country_data, country) :
    areas = []
    for x in country_data :
        areas.append(int(x.get('Area')))
        if (x.get('Country') == country) :
            country_area = int(x.get('Area'))

    areas.sort(reverse=True)
    country_rank = 1
    for x in areas :
        if (x == country_area) :
            return country_rank
        else :
            country_rank = country_rank + 1


def getCountryPopulationData(populations, country_name) :
    countryPopulation = []
    for x in populations :
        if (x.get('Country') == country_name) :
            countryPopulation.append(
                        {
                            'Year': x.get('Year'),
                            'Population': x.get('Population')
                        }
                    )

    return countryPopulation



def getPopulation(population_data, year) :
    for x in population_data :
        if (x.get('Year') == str(year)) :
            return x.get('Population')



def getYearlyPopRank(data, country, year) :
    sortedPops = []
    for x in data :
        if (x.get('Year') == str(year)) :
            if (x.get('Country') == country) :
                my_pop = x.get('Population')
            sortedPops.append(int(x.get('Population')))

    sortedPops.sort(reverse=True)
    my_rank = 1
    for x in sortedPops :
        if (x == int(my_pop)) :
            return my_rank
        else :
            my_rank = my_rank + 1


def getDensityRank(data, country_name, year, country_data) :
    sortedRanks = []
    for x in data :
        if (x.get('Year') == str(year)) :
            if (x.get('Country') == country_name) :
                for y in country_data :
                    if (y.get('Country') == country_name) :
                        my_density = int(int(x.get('Population')) / int(y.get('Area')))
            tempCountry = x.get('Country')
            tempPop = int(x.get('Population'))
            for y in country_data :
                if (y.get('Country') == tempCountry) :
                    tempDensity = tempPop / int(y.get('Area'))
                    sortedRanks.append(int(tempDensity))

    sortedRanks.sort(reverse=True)
    my_rank = 1
    for x in sortedRanks :
        if (my_density == x) :
            return my_rank
        else:
            my_rank = my_rank + 1



def getCountryGDPData(data, country_name) :
    gdp_data = []
    for x in data :
        if (x.get('Country') == country_name) :
            gdp_data.append(
                        {
                            'Year': x.get('Year'),
                            'gdppc': x.get('gdppc'),
                            'Currency': x.get('Currency')
                        }
                    )
    return gdp_data



def getGDPPC(data, year) :
    for x in data :
        if (x.get('Year') == str(year)) :
            return x.get('gdppc')



def getGDPRank(data, country_name, year) :
    sortedRanks = []
    for x in data :
        if (x.get('Year') == str(year)) :
            if (x.get('Country') == country_name) :
                my_gdppc = x.get('gdppc')
            sortedRanks.append(x.get('gdppc'))

    sortedRanks.sort(reverse=True)
    my_rank = 1
    for x in sortedRanks :
        if (x == my_gdppc) :
            return my_rank
        else :
            my_rank = my_rank + 1



def reportA(dynamodb, country_name) :
    country_data = getItems(dynamodb, 'gnodwell_country_data')
    codes_data = getItems(dynamodb, 'UN_country_codes')
    all_population_data = getItems(dynamodb, 'gnodwell_population_data')
    population_data = getCountryPopulationData(all_population_data, country_name)
    all_gdp_data = getItems(dynamodb, 'gnodwell_gdp_data')
    gdp_data = getCountryGDPData(all_gdp_data, country_name)

    areaRank = calcAreaRank(country_data, country_name)
    for x in codes_data:
        if (x.get('name') == country_name) :
            offical_name = x.get('name')
    for x in country_data:
        if (x.get('Country') == country_name) :

            print("Name of Country: ", x.get('Country'))
            print("[Official Name: ", offical_name+']')
            print('\n')
            my_area = x.get('Area')
            print("Area: ", x.get('Area'), "sq km ", '(World Rank: '+str(areaRank)+')')
            if (x.get("Language 1") != '') :
                langs = x.get("Language 1")
            if (x.get('Language 2') != '') :
                langs = langs + ' / ' + x.get('Language 2')
            if (x.get("Language 3") != '') :
                langs = langs + ' / ' + x.get('Language 3')
            print("Offical/Nation Languages: ", langs)
            print("Capital City: ", x.get("Capital"))
            print('\n')

    print("Population")
    print("Year             Population            Rank            Population Density(people/sq km)            Rank")
    for x in range(50) :
        hold12 = round(int(getPopulation(population_data, x+1970))/(int(my_area)), 2)
        try :
            print(x+1970, " "*(15-len(str(x+1970))), getPopulation(population_data, x+1970), " "*(20-len(str(getPopulation(population_data, x+1970)))),
                    getYearlyPopRank(all_population_data, country_name, x+1970), " "*(14-len(str(getYearlyPopRank(all_population_data, country_name, x+1970)))),
                    hold12, " "*(42-len(str(hold12))), getDensityRank(all_population_data, country_name, x+1970, country_data))
        except Exception as e:
            thisSucks=0

    print("\n")
    print("Economics")
    print("Currency: ", gdp_data[0].get('Currency'))
    print('\n')
    print("Year             GDPPC           Rank")
    for x in range(50):
        print(x+1970, " "*(15-len(str(x+1970))), getGDPPC(gdp_data, x+1970)," "*(14-len(getGDPPC(gdp_data, x+1970))), getGDPRank(all_gdp_data, country_name, x+1970))





def getAllRankedPopulation(data, year) :
    sortedPopRank = []
    for x in data :
        if (x.get('Year') == str(year)) :
            hold = {
                    'Country': x.get('Country'),
                    'Population': int(x.get('Population')),
                    'Year': x.get('Year')
                    }
            sortedPopRank.append(hold)

    sortedPopRank = sorted(sortedPopRank, key=lambda d: d['Population'], reverse=True)
    return sortedPopRank



def getAllRankedArea(data, year) :
    sortedArea = []
    for x in data :
        hold = {
                'Country': x.get('Country'),
                'Area': int(x.get('Area'))
                }
        sortedArea.append(hold)

    sortedArea = sorted(sortedArea, key=lambda d: d['Area'], reverse=True)
    return sortedArea



def getAllRankedDensity(c_data, pop_data, year) :
    sortedDensity = []
    for x in c_data:
        for y in pop_data:
            if (x.get("Country") == y.get("Country")) :
                if (y.get("Year") == str(year)) :
                    tempDensity = int(y.get('Population')) / int(x.get('Area'))
                    tempDensity = round(tempDensity, 2)
                    hold = {
                            'Country': x.get('Country'),
                            'Density': tempDensity
                            }
                    sortedDensity.append(hold)

    sortedDensity = sorted(sortedDensity, key=lambda d: d['Density'], reverse=True)
    return sortedDensity



def getTenYearInt(data, country, year) :
    hold = {
            'Country': '',
            '1': '',
            '2': '',
            '3': '',
            '4': '',
            '5': '',
            '6': '',
            '7': '',
            '8': '',
            '9': '',
            '10': ''
            }
    for x in data :
        if (x.get("Country") == country) :
            hold['Country'] = x.get('Country')
            if (x.get('Year') == str(year)) :
                hold['1'] = x.get('gdppc')
            if (x.get('Year') == str(year+1)) :
                hold['2'] = x.get('gdppc')
            if (x.get('Year') == str(year+2)) :
                hold['3'] = x.get('gdppc')
            if (x.get('Year') == str(year+3)) :
                hold['4'] = x.get('gdppc')
            if (x.get('Year') == str(year+4)) :
                hold['5'] = x.get('gdppc')
            if (x.get('Year') == str(year+5)) :
                hold['6'] = x.get('gdppc')
            if (x.get('Year') == str(year+6)) :
                hold['7'] = x.get('gdppc')
            if (x.get('Year') == str(year+7)) :
                hold['8'] = x.get('gdppc')
            if (x.get('Year') == str(year+8)) :
                hold['9'] = x.get('gdppc')
            if (x.get('Year') == str(year+9)) :
                hold['10'] = x.get('gdppc')
    return hold






def reportB(dynamodb, year) :
    country_data = getItems(dynamodb, 'gnodwell_country_data')
    all_population_data = getItems(dynamodb, 'gnodwell_population_data')
    all_gdp_data = getItems(dynamodb, 'gnodwell_gdp_data')

    num_countries = 0
    for x in country_data :
        num_countries = num_countries + 1

    rankedPopulation = getAllRankedPopulation(all_population_data, year)
    my_index = 1

    rankedArea = getAllRankedArea(country_data, year)

    rankedDensity = getAllRankedDensity(country_data, all_population_data, year)

    print("Year: ", year)
    print("Number of Countries: ", num_countries)
    print('\n')
    print("Table of Countries Ranked by Population (largest to smallest)")
    print("Country Name", " "*28, "Population", " "*20, "Rank")
    for x in rankedPopulation :
        print(x.get('Country'), " "*(40-len(x.get("Country"))), x.get('Population'), " "*(30-len(str(x.get("Population")))) , my_index)
        my_index = my_index + 1

    my_index = 1
    print("\n")
    print("Tables of Countries Ranked by Area (largest to Smallest)")
    print("Country Name", " "*28, "Area (sq km)", " "*20, "Rank")
    for x in rankedArea :
        print(x.get('Country'), " "*(40-len(x.get("Country"))), x.get('Area'), " "*(32-len(str(x.get("Area")))) , my_index)
        my_index = my_index + 1

    print('\n')
    print("Tables of Countries Ranked by Density (largest to smallest)")
    print("Country Name", " "*28, "Density (people / sq km)", " "*20, "Rank")
    my_index = 1
    for x in rankedDensity :
        print(x.get('Country'), " "*(40-len(x.get("Country"))), x.get('Density'), " "*(44-len(str(x.get("Density")))) , my_index)
        my_index = my_index + 1
    print('\n')
    print("GDP Per Capita for all Countries")
    print_year = 1970
    year_counter = 1970
    for x in range(5):
        yearStr = str(print_year)
        yearStr = yearStr.strip()
        yearStr = yearStr + "\'s Table"
        print(yearStr)
        print('Country Name', " "*(40-len('Country Name')), year_counter, " "*6, year_counter+1, " "*6, year_counter+2, " "*6, year_counter+3, " "*6, year_counter+4,
                    " "*6, year_counter+5, " "*6, year_counter+6, " "*6, year_counter+7, " "*6, year_counter+8, " "*6, year_counter+9)
        for z in country_data :



            hold = getTenYearInt(all_gdp_data, z.get('Country'), year_counter)


            print(hold.get('Country'), " "*(40-len(hold.get('Country'))), hold.get('1'), " "*(10-len(str(hold.get('1')))), hold.get('2'), " "*(10-len(str(hold.get('2')))),
                   hold.get('3'), " "*(10-len(str(hold.get('3')))), hold.get('4'), " "*(10-len(str(hold.get('4')))), hold.get('5'), " "*(10-len(str(hold.get('5')))),
                   hold.get('6'), " "*(10-len(str(hold.get('6')))), hold.get('7'), " "*(10-len(str(hold.get('7')))), hold.get('8'), " "*(10-len(str(hold.get('8')))),
                   hold.get('9'), " "*(10-len(str(hold.get('9')))), hold.get('10'), " "*(10-len(str(hold.get('10')))))

        print_year = print_year + 10
        year_counter = year_counter + 10


        print("\n")



def getItems(dynamodb, table_name) :
    try :
        table = dynamodb.Table(table_name)
        response = table.scan()
        data = response['Items']
        return (data)
    except Exception as e:
        print(e)
        return -1



#main

fp = open("credentials", "r")




lines = fp.readlines()
for x in lines:
    hold = x.split(" ")
    if (hold[0] == 'aws_access_key_id') :
        access_key = hold[2].strip('\n')
    elif (hold[0] == 'aws_secret_access_key') :
        secret_access = hold[2].strip('\n')




session = boto3.Session(region_name='ca-central-1', aws_access_key_id=access_key, aws_secret_access_key=secret_access)
dynamodb = session.resource('dynamodb', region_name='ca-central-1')

while (True) :
    usrInput = input("What would you like to do ('ReportA', 'ReportB', 'quit'): ")
    if (usrInput == 'quit') :
        exit (0)
    elif (usrInput == 'ReportA') :
        country = input("What country would you like to report (must start with a capital ex ('Canada')): ")
        try :
            reportA(dynamodb, country)
        except Exception as e:
            print("Unable to print ReportA")
            print(e)
    elif (usrInput == "ReportB") :
        year = input("What year would you like to report (1970-2019) or (All): ")
        if (int(year) < 1970 or int(year) > 2019) :
            print("Unable to access information from that year")
            exit(0)
        if (year == "All") :
            for x in range (1970, 2019) :
                try :
                    reportB(dynamodb, x)
                except Exception as e:
                    print("Unable to print ReportB")

        else :
            try :
                reportB(dynamodb, int(year))
            except Exception as e:
                print("Unable to print ReportB")


    else :
        print("Unexpected User Input")

