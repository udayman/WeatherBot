import CYKParse
import Tree

import json
import urllib.parse
import urllib.request

import datetime
import random

requestInfo = {
        'name': '',
        'timeone': '',
        'timeoneaugment': '',
        'location': '',
        'timetwo': '',
        'timetwoaugment': '',
        'temperatureq': '',
        'comparison': '',
        'set': '',
        'settemp': '',
        'metric': '',
        'sethomelocation': '',
        'addlocation': '',
        'latitude': '',
        'longitude': '',
        'sunsettime': '',
        'sunrisetime': '',
        'any': '',
        'alerts': '',
        'you': '',
        'botname': '',
        'botfavweather': '',
        'botcity': '',
        'botage': '',
        'randomcity': '',
        'rain': '',
        'snow': '',
        
}


locations = {
    'Irvine': ('33.669445', '-117.823059'),
    'Tustin': ('33.7458511', '-117.826166'),
    'Pasadena': ('34.156113', '-118.131943'),
    'Austin': ('30.266668', '-97.733330'),
    'Seattle': ('47.608013', '-122.335167'),
    'Fremont': ('37.548271', '-121.988571'),
    'Kolkata': ('22.572645', '88.363892'),
    'Sacramento': ('38.575764', '-121.478851'),
    'Reno': ('39.530895', '-119.814972'),
    'Asansol': ('23.673944', '86.952393'),
    'Portland': ('45.523064', '-122.676483'),
    'San Francisco': ('37.773972', '-122.431297'),
    'New York City': ('40.730610', '-73.935242'),
    'San Antonio': ('29.424349', '-98.491142'),
    'home': (),
}

personalDetails = {
    'home': '',
    'metric': '',
}



def generateAPIInfo(location, info, metric, time='today', timedetail=''):
    answer = None
    
    #note temperatures are returned as integers
    if (info == 'givealert'):
        url = "https://api.openweathermap.org/data/2.5/onecall?" + urllib.parse.urlencode([('lat', locations[location][0]),('lon', locations[location][1]), ('units', metric), ('appid', '0bb2c8b8f51f03a3b08d013632ecfc7a')])
        try:
            answer = urllib.request.urlopen(url)
            text = answer.read().decode(encoding = 'utf-8')
            if "alerts" in json.loads(text).keys():
                return json.loads(text)["alerts"][0]["description"]
            else:
                return "none"
        except:
            return 'error'
        finally:
            if (answer != None):
                answer.close()

    elif (time == 'today' or time == 'now'):
        url = "https://api.openweathermap.org/data/2.5/onecall?" + urllib.parse.urlencode([('lat', locations[location][0]),('lon', locations[location][1]), ('units', metric), ('appid', '0bb2c8b8f51f03a3b08d013632ecfc7a')])
        if (info == 'temperature'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if (timedetail == ''):
                    return (json.loads(text)["current"]["temp"])
                elif (timedetail == 'evening'):
                    return (json.loads(text)["daily"][0]["temp"]["eve"])
                elif (timedetail == 'morning'):
                    return (json.loads(text)["daily"][0]["temp"]["morn"])
                elif (timedetail == 'afternoon'):
                    return (json.loads(text)["daily"][0]["temp"]["day"])
                elif (timedetail == 'nighttime'):
                    return (json.loads(text)["daily"][0]["temp"]["night"])
                    
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()
                    
        elif (info == 'rain'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if "rain" in json.loads(text)["daily"][0].keys():
                    return json.loads(text)["daily"][0]["rain"]
                return 0
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'snow'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if "snow" in json.loads(text)["daily"][0].keys():
                    return json.loads(text)["daily"][0]["snow"]
                return 0
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'sunrise'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                unix = json.loads(text)["daily"][0]["sunrise"]
                return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'sunset'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                unix = json.loads(text)["daily"][0]["sunset"]
                return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()
            
                    
    elif (time == "tomorrow"):
        url = "https://api.openweathermap.org/data/2.5/onecall?" + urllib.parse.urlencode([('lat', locations[location][0]),('lon', locations[location][1]), ('units', metric), ('appid', '0bb2c8b8f51f03a3b08d013632ecfc7a')])
        if (info == 'temperature'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if (timedetail == 'evening'):
                    return (json.loads(text)["daily"][1]["temp"]["eve"])
                elif (timedetail == 'morning'):
                    return (json.loads(text)["daily"][1]["temp"]["morn"])
                elif (timedetail == 'afternoon' or timedetail == ''):
                    return (json.loads(text)["daily"][1]["temp"]["day"])
                elif (timedetail == 'nighttime'):
                    return (json.loads(text)["daily"][1]["temp"]["night"])
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'rain'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if "rain" in json.loads(text)["daily"][1].keys():
                    return json.loads(text)["daily"][1]["rain"]
                return 0
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'snow'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if "snow" in json.loads(text)["daily"][1].keys():
                    return json.loads(text)["daily"][1]["snow"]
                return 0
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'sunrise'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                unix = json.loads(text)["daily"][1]["sunrise"]
                return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'sunset'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                unix = json.loads(text)["daily"][1]["sunset"]
                return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

    elif (time == "yesterday"):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
        yesterday = str(int(yesterday))
        url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?" + urllib.parse.urlencode([('lat', locations[location][0]),('lon', locations[location][1]), ('dt', yesterday), ('units', metric), ('appid', '0bb2c8b8f51f03a3b08d013632ecfc7a')])
        if (info == 'temperature'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                return (json.loads(text)["current"]["temp"])
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'rain'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if "rain" in json.loads(text)["current"].keys():
                    return json.loads(text)["current"]["rain"]
                return 0
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'snow'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                if "snow" in json.loads(text)["current"].keys():
                    return json.loads(text)["current"]["snow"]
                return 0
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'sunrise'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                unix = json.loads(text)["current"]["sunrise"]
                return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()

        elif (info == 'sunset'):
            try:
                answer = urllib.request.urlopen(url)
                text = answer.read().decode(encoding = 'utf-8')
                unix = json.loads(text)["current"]["sunset"]
                return datetime.datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
            except:
                return 'error'
            finally:
                if (answer != None):
                    answer.close()


# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    #returns '' on failure instead of causing error in max
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') }
    if len(sentenceTrees) == 0:
        return ''
    completeSentenceTree = max(sentenceTrees.keys(), key = lambda x: int(x[4:]))
    #print('getSentenceParse', completeSentenceTree)
    return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    #reset all values
    for key in requestInfo.keys():
        if key != 'location': #we want to preserve location for later sentences
            requestInfo[key] = ''
        
    for leaf in Tr.getLeaves():
        #added below if statement
        if (leaf[1] == 'today' or leaf[1] == 'yesterday' or leaf[1] == 'tomorrow' or leaf[1] == 'now'):
            if requestInfo['timeone'] == '':
                requestInfo['timeone'] = leaf[1]
            elif requestInfo['timetwo'] == '':
                requestInfo['timetwo'] = leaf[1]

        if (leaf[1] == 'evening' or leaf[1] == 'morning' or leaf[1] == 'afternoon' or leaf[1] == 'nighttime'):
            if requestInfo['timetwo'] == '':
                requestInfo['timeoneaugment'] = leaf[1]
            else:
                requestInfo['timetwoaugment'] = leaf[1]

        if (leaf[1] == 'your'):
            requestInfo['you'] = True

        if (requestInfo['you'] == True and leaf[1] == 'name'):
            requestInfo['botname'] = True

        if (requestInfo['you'] and leaf[1] == 'favorite'):
            requestInfo['botfavweather'] = True

        if (requestInfo['you'] and leaf[1] == 'age'):
            requestInfo['botage'] = True

        if (requestInfo['you'] and leaf[1] == 'city' and requestInfo['botfavweather'] == ''):
            requestInfo['botcity'] = True

        if (leaf[1] == 'add' and leaf[0] == 'Verb'):
            requestInfo['addlocation'] = True

        if (leaf[1] == 'random'):
            requestInfo['randomcity'] = True
            
        if (leaf[1] == 'sunrise' and leaf[0] == 'Noun'):
            requestInfo['sunrisetime'] = True
            
        if (leaf[1] == 'sunset' and leaf[0] == 'Noun'):
            requestInfo['sunsettime'] = True

        if (leaf[1] == 'imperial' or leaf[1] == 'metric' or leaf[1] == 'standard'):
            requestInfo['metric'] = leaf[1]
                
        if requestInfo['set'] and leaf[0] == 'Name' and leaf[1] == 'home':
            requestInfo['sethomelocation'] = True
        elif leaf[0] == 'Name' and (' '.join(leaf[1].split('.')) in locations.keys()):
            requestInfo['location'] = ' '.join(leaf[1].split('.'))

        if leaf[0] == 'Noun' and (leaf[1] == 'alert' or leaf[1] == 'alerts'):
            requestInfo['alerts'] = True

        if (leaf[1] == 'any'):
            requestInfo['any'] = True

        if (leaf[0] == 'Noun' and leaf[1] == 'rain'):
            requestInfo['rain'] =  True
        if (leaf[0] == 'Noun' and leaf[1] == 'snow'):
            requestInfo['snow'] = True
            
        if leaf[0] == 'Noun' and leaf[1] == 'temperature':
            requestInfo['temperatureq'] = True
        if leaf[0] == 'Adjective' and (leaf[1] == 'hotter' or leaf[1] == 'colder' or leaf[1] == 'warmer'):
            requestInfo['comparison'] = leaf[1]
        if leaf[0] == 'Verb' and leaf[1] == 'set':
            requestInfo['set'] = True



# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo

    if (requestInfo['metric'] != ''):
        personalDetails['metric'] = requestInfo['metric']
    metric = 'imperial'
    if (personalDetails['metric'] != ''):
        metric = personalDetails['metric']

    if (metric == 'imperial'):
        units = 'Fahrenheit'
    elif (metric == 'standard'):
        units = 'Kelvin'
    elif (metric == 'metric'):
        units = 'Celsius'

    #setting reply "is" cases
    if (requestInfo['timeone'] == 'now' or requestInfo['timeone'] == 'today'):
        isWord = ' is '
    elif (requestInfo['timeone'] == 'yesterday'):
        isWord = ' was '
    elif (requestInfo['timeone'] == 'tomorrow'):
        isWord = ' will be '

    if (requestInfo['timetwo'] == 'now' or requestInfo['timetwo'] == 'today'):
        isWordTwo = ' is '
    elif (requestInfo['timetwo'] == 'yesterday'):
        isWordTwo = ' was '
    elif (requestInfo['timetwo'] == 'tomorrow'):
        isWordTwo = ' will be '

    #reply if statements

    #for setting metric
    if (requestInfo['set'] == True and requestInfo['metric'] != ''):
        if (random.randint(0,1) == 0):
            print('Your temperature preference has been set to ' + metric + '.')
        else:
            print('I have successfully set your temperature preference. It is now: ' + metric + '.')
        return

    #for adding location
    elif (requestInfo['addlocation'] == True):
        print("Enter your location name, and please use correct capitalization.")
        city = input().strip()

        print("Enter the longitude for " + city + ".")
        longitude = input().strip()

        print("Enter the latitude for " + city + ".")
        latitude = input().strip()

        location = (longitude, latitude)

        locations[city] = location

        if (random.randint(0,1) == 0):
            print("Now, your city " + city + " was set in the database.")

        else:
            print("Success! " + city + " is now in the database.")

    #for getting bot name
    elif (requestInfo['botname']):
        if (random.randint(0,1) == 0):
            print("Hi there, my name is Raja.")
        else:
            print("My name is Raja, nice to meet you.")

    #for getting bot favorite location
    elif (requestInfo['botfavweather']):
        if (random.randint(0,1) == 0):
            print("My favorite city is Fremont, since it never snows there, and is always sunny.")
        else:
            print("I love Fremont the most, because it is never too cold or too hot there.")

    #for getting bot location
    elif (requestInfo['botcity']):
        if (random.randint(0,1) == 0):
            print("My current location is Irvine.")
        else:
            print("I am a bot living in Irvine, created in UC Irvine.")

    #for getting bot age
    elif (requestInfo['botage']):
        if (random.randint(0,1) == 0):
            print("My current age is 10 weeks.")
        else:
            print("I am 10 weeks old currently.")

    #for getting random city
    elif (requestInfo['randomcity']):
        city = random.choice(list(locations.keys()))

        if (random.randint(0,1) == 0):
            print("Here is a random city: " + city + ".")
        else:
            print("A random city in our database is " + city + ".") 
        

    #for temperature
    elif (requestInfo['temperatureq'] == True and requestInfo['timeone'] != '' and requestInfo['timetwo'] == '' and requestInfo['location'] != ''):
        if (requestInfo['location'] == 'home' and personalDetails['home'] == ''):
            if (random.randint(0,1) == 0):
                print("Unfortunately, no location is set for your home.")
            else:
                print("Sorry, I could not find a set location for your home.")
            return
        temp = generateAPIInfo(requestInfo['location'], 'temperature', metric, requestInfo['timeone'], requestInfo['timeoneaugment'])
        if (temp == 'error'):
            if (random.randint(0,1) == 0):
                print('Unfortunately, the API failed to provide your temperature for the city ' + requestInfo['location'] + '.')
            else:
                print('Loading...API loading failed. Could not provide temperature for the city ' + requestInfo['location'] + '.')
            return

        if (requestInfo['timeone'] == 'yesterday' or requestInfo['timeoneaugment'] == ''):
            requestInfo['timeoneaugment'] = 'at this time'
        if (random.randint(0,1) == 0):
            print('The temperature in ' + requestInfo['location'] + ' ' + requestInfo['timeone'] + ' ' + requestInfo['timeoneaugment'] + isWord + str(temp) + ' ' + units + '.')
        else:
            print('Temperature in ' + requestInfo['location'] + ' ' + requestInfo['timeone'] + ' ' + requestInfo['timeoneaugment'] + ': ' + str(temp) + ' ' + units + '.')
    #no location for temperature
    elif (requestInfo['temperatureq'] == True and requestInfo['timeone'] != '' and requestInfo['timetwo'] == '' and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I cannot figure out which location you are asking about. Kindly tell me which location you would like.')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()

    #for sunrise or sunset
    elif ((requestInfo['sunrisetime'] == True or requestInfo['sunsettime'] == True) and requestInfo['timeone'] != '' and requestInfo['location'] != ''):
        if (requestInfo['location'] == 'home' and personalDetails['home'] == ''):
            if (random.randint(0,1) == 0):
                print("Unfortunately, no location is set for your home.")
            else:
                print("Sorry, I could not find a set location for your home.")

        if requestInfo['sunsettime']:
            time = generateAPIInfo(requestInfo['location'], 'sunset', metric, requestInfo['timeone'], requestInfo['timeoneaugment'])
        else:
            time = generateAPIInfo(requestInfo['location'], 'sunrise', metric, requestInfo['timeone'], requestInfo['timeoneaugment'])
            
        if (time == 'error'):
            if (random.randint(0,1) == 0):
                print('Unfortunately, the API failed to provide your time for the city ' + requestInfo['location'] + '.')
            else:
                print('Loading...API loading failed. Could not provide time for the city ' + requestInfo['location'] + '.')

        if (requestInfo['sunsettime']):
            if (random.randint(0,1) == 0):
                print("Sunset time in " + requestInfo['location'] + " " + requestInfo['timeone'] + ": " + time + ".")
            else:
                print("In " + requestInfo['location'] + " " + requestInfo['timeone'] + " the sunset time is " + time + ".")
        else:
            if (random.randint(0,1) == 0):
                print("Sunrise time in " + requestInfo['location'] + " " + requestInfo['timeone'] + ": " + time + ".")
            else:
                print("In " + requestInfo['location'] + " " + requestInfo['timeone'] + " the sunrise time is " + time + ".")

    #no location for sunrise or sunset
    elif (requestInfo['sunrisetime'] == True or requestInfo['sunsettime'] == True and requestInfo['timeone'] != '' and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I cannot figure out which location you are asking about. Kindly tell me which location you would like.')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()

    #for rain
    elif (requestInfo['timeone'] != '' and requestInfo['timetwo'] == '' and requestInfo['rain'] == True and requestInfo['location'] != ''):
        if (requestInfo['location'] == 'home' and personalDetails['home'] == ''):
            if (random.randint(0,1) == 0):
                print("Unfortunately, no location is set for your home.")
            else:
                print("Sorry, I could not find a set location for your home.") 
            return
        
        rain = generateAPIInfo(requestInfo['location'], 'rain', metric, requestInfo['timeone'], requestInfo['timeoneaugment'])
        if (rain == 'error'):
            if (random.randint(0,1) == 0):
                print('Unfortunately, the API failed to provide your rain for the city ' + requestInfo['location'] + '.')
            else:
                print('Loading...API loading failed. Could not provide rain for the city ' + requestInfo['location'] + '.')
            return
                
        if (random.randint(0,1) == 0):
            print('The rain amount in ' + requestInfo['location'] + ' ' + requestInfo['timeone'] + isWord + str(rain) + ' mm.')
        else:
            print('Rain amount in ' + requestInfo['location'] + ' ' + requestInfo['timeone'] + ' ' + ': ' + str(rain) + ' mm.')
    #no location for rain
    elif (requestInfo['timeone'] != '' and requestInfo['rain'] == True and  requestInfo['timetwo'] == '' and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I cannot figure out which location you are asking about. Kindly tell me which location you would like.')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()

    #for snow
    elif (requestInfo['timeone'] != '' and requestInfo['timetwo'] == '' and requestInfo['snow'] == True and requestInfo['location'] != ''):
        if (requestInfo['location'] == 'home' and personalDetails['home'] == ''):
            if (random.randint(0,1) == 0):
                print("Unfortunately, no location is set for your home.")
            else:
                print("Sorry, I could not find a set location for your home.") 
            return
        
        snow = generateAPIInfo(requestInfo['location'], 'snow', metric, requestInfo['timeone'], requestInfo['timeoneaugment'])
        if (snow == 'error'):
            if (random.randint(0,1) == 0):
                print('Unfortunately, the API failed to provide your snow for the city ' + requestInfo['location'] + '.')
            else:
                print('Loading...API loading failed. Could not provide snow for the city ' + requestInfo['location'] + '.')
            return
                
        if (random.randint(0,1) == 0):
            print('The snow amount in ' + requestInfo['location'] + ' ' + requestInfo['timeone'] + isWord + str(snow) + ' mm.')
        else:
            print('Snow amount in ' + requestInfo['location'] + ' ' + requestInfo['timeone'] + ' ' + ': ' + str(snow) + ' mm.')
    #no location for snow
    elif (requestInfo['timeone'] != '' and requestInfo['snow'] == True and requestInfo['timetwo'] == '' and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I cannot figure out which location you are asking about. Kindly tell me which location you would like.')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()
    

    #for alerts
    elif (requestInfo['alerts'] == True and requestInfo['location'] != ''):
        if (requestInfo['location'] == 'home' and personalDetails['home'] == ''):
            if (random.randint(0,1) == 0):
                print("Unfortunately, no location is set for your home.")
            else:
                print("I couldn't find a location for your home.")
            return
        alert = generateAPIInfo(requestInfo['location'], 'givealert', metric)
        if (alert == 'error'):
            if (random.randint(0,1) == 0):
                print('Unfortunately, the API failed to provide your alert for the city ' + requestInfo['location'] + '.')
            else:
                print('Loading...API loading failed. Could not provide alerts for the city ' + requestInfo['location'] + '.')
            return
        if (alert == 'none'):
            if (random.randint(0,1) == 0):
                print("No alert was found in " + requestInfo['location'] + ".")
            else:
                print("I looked far and wide, but no alert in " + requestInfo['location'] + ".")
        else:
            if (requestInfo['any'] == True):
                if (random.randint(0,1) == 0):
                    print("There are alerts in " + requestInfo['location'] + ".")
                else:
                    print("Warning! I have found alerts in " + requestInfo['location'] + ".")
            else:
                if (random.randint(0,1) == 0):
                    print("Here is the most important alert in " + requestInfo['location'] + ":\n")
                    print(alert)
                else:
                    print("I found an alert! In " + requestInfo['location'] + ":\n")
                    print(alert)
    #no location for alerts
    elif (requestInfo['alerts'] == True and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I cannot figure out which location you are asking about. Kindly tell me which location you would like.')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()

    #for setting home location
    elif (requestInfo['sethomelocation'] == True and requestInfo['location'] != ''):
        if (random.randint(0,1) == 0):
            print('Your home location has been currently set to ' + requestInfo['location'] + '.')
        else:
            print('I have managed to set your home location to ' + requestInfo['location'] + '.')
        personalDetails['home'] = requestInfo['location']
        locations['home'] = locations[requestInfo['location']]

    #no location for setting home
    elif (requestInfo['sethomelocation'] == True and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I cannot figure out which location you are asking about. Kindly tell me which location you would like.')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()

    #for comparison temperatures
    elif (requestInfo['timeone'] != '' and requestInfo['timetwo'] != '' and requestInfo['comparison'] != '' and requestInfo['location'] != ''):
        #since hotter check timeone > timetwo
        if (requestInfo['location'] == 'home' and personalDetails['home'] == ''):
            if (random.randint(0,1) == 0):
                print("Unfortunately, no location is set for your home.")
            else:
                print("Sorry, I could not find a set location for your home.")
            return
        tempone = generateAPIInfo(requestInfo['location'], 'temperature', metric, requestInfo['timeone'], requestInfo['timeoneaugment'])
        temptwo = generateAPIInfo(requestInfo['location'], 'temperature', metric, requestInfo['timetwo'], requestInfo['timetwoaugment'])
        if (tempone == 'error' or temptwo == 'error'):
            if (random.randint(0,1) == 0):
                print('Unfortunately, the API failed to provide your temperature for the city ' + requestInfo['location'] + '.')
            else:
                print('Loading...API loading failed. Could not provide temperature for the city ' + requestInfo['location'] + '.')
            return
        if (requestInfo['comparison'] == 'hotter' or requestInfo['comparison'] == 'warmer'):
            truth_value = tempone > temptwo
        else:
            truth_value = tempone < temptwo

        if (requestInfo['timeone'] == 'yesterday' or requestInfo['timeoneaugment'] == ''):
            if (random.randint(0,1) == 0):
                requestInfo['timeoneaugment'] = 'at this time'
            else:
                requestInfo['timeoneaugment'] = 'at the current time'

        if (requestInfo['timetwo'] == 'yesterday' or requestInfo['timetwoaugment'] == ''):
            if (random.randint(0,1) == 0):
                requestInfo['timeoneaugment'] = 'at this time'
            else:
                requestInfo['timeoneaugment'] = 'at the current time'
            
        ending_sentiment = 'since the temperature in ' + \
                  requestInfo['location'] + ' ' + requestInfo['timeone'] + ' ' + requestInfo['timeoneaugment'] + isWord + \
                  str(tempone) + ' ' + units + \
                  ' while the temperature ' + requestInfo['timetwo'] + ' ' + requestInfo['timetwoaugment'] + isWordTwo + \
                  str(temptwo) + ' ' + units + \
                  '.'
        if truth_value:
            if (random.randint(0,1) == 0):
                print('Yes, it will be, ' + ending_sentiment)
            else:
                print('Indeed, here is my analysis: ' + ending_sentiment)
        else:
            if (random.randint(0,1) == 0):
                print('No, it will not be, ' + ending_sentiment)
            else:
                print('No, here is my analysis: ' + ending_sentiment)

    #for no location for comparison    
    elif (requestInfo['timeone'] != '' and requestInfo['timetwo'] != '' and requestInfo['comparison'] != '' and requestInfo['location'] == ''):
        if (random.randint(0,1) == 0):
            print('There is no location currently set so I do not know which city you would like to know your information. Perhaps you can tell me which one?')
        else:
            print('Sorry, I could not determine the city you are interested in. Maybe you could tell me?')

        city = input()
        city = city.strip()
        if (city not in locations.keys()):
            if (random.randint(0,1) == 0):
                print('Your city ' + city + ' is unrecognizable.')
            else:
                print(city + ' was not found in our locations database.')
        else:
            requestInfo['location'] = city
            reply()

    #final error case
    else:
        if (random.randint(0,1) == 0):
            print('You have not requested a sentence that I can understand, since I am not that intelligent.')
        else:
            print('Sorry I could not understand your request. Unfortunately my human overlords have blessed me with a limited vocabulary.')



# A simple hard-coded proof of concept.
def main():
    global requestInfo

    #CYKParse.verbose = True
    #CYKParse.CYKParse(['add', 'a', 'city', 'to', 'the', 'database'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['what', 'is', 'your', 'city'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['tell', 'me', 'a', 'random', 'city', 'in', 'your', 'database'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['what', 'is', 'your', 'name'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['which', 'city' , 'is', 'your', 'favorite'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['which', 'city' , 'has', 'your', 'favorite', 'weather'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['when', 'is', 'sunrise', 'tomorrow', 'morning'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['set', 'the', 'temperature', 'to', 'metric'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'tomorrow'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['tomorrow', 'morning', 'hotter', 'than', 'today', 'nighttime', 'in', 'Irvine'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['set', 'Tustin', 'to', 'home'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['is', 'there', 'rain', 'in', 'Irvine', 'yesterday'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['rain', 'in', 'Irvine', 'yesterday'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['rain', 'amount', 'in', 'Irvine', 'yesterday'], CYKParse.getGrammarWeatherCustomLocations(locations))
    #CYKParse.CYKParse(['what', 'is', 'be', 'the', 'rain', 'amount', 'in', 'Irvine', 'yesterday'], CYKParse.getGrammarWeatherCustomLocations(locations))

    T,P = CYKParse.CYKParse(['what', 'is', 'your', 'name'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['which', 'city' , 'is', 'your', 'favorite'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T,P = CYKParse.CYKParse(['tell', 'me', 'a', 'random', 'city', 'in', 'your', 'database'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T,P = CYKParse.CYKParse(['what', 'is', 'your', 'age'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'your', 'city'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    '''
    T,P = CYKParse.CYKParse(['add', 'a', 'city', 'to', 'the', 'database'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'San', 'Ramon', 'now'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T,P = CYKParse.CYKParse(['when', 'is', 'sunrise', 'in', 'Irvine', 'yesterday', 'night'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T,P = CYKParse.CYKParse(['temperature', 'tomorrow', 'evening'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T,P = CYKParse.CYKParse(['are', 'there', 'any', 'weather', 'alerts', 'in', 'Irvine'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T,P = CYKParse.CYKParse(['tell', 'me', 'a', 'weather', 'alert', 'in', 'Irvine'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    
    T, P = CYKParse.CYKParse(['set', 'my', 'home', 'to', 'Tustin'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'San Francisco', 'now'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'now'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'Pasadena', 'tomorrow'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()
    
    T, P = CYKParse.CYKParse(['what', 'was', 'the', 'temperature', 'in', 'Tustin', 'yesterday'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'is', 'the', 'temperature', 'in', 'home', 'yesterday', 'afternoon'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    
    T, P = CYKParse.CYKParse(['will', 'tomorrow', 'morning', 'be', 'hotter', 'than', 'today', 'nighttime' 'in', 'Tustin'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'tomorrow', 'evening', 'be', 'warmer', 'than', 'now', 'in', 'Tustin'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'now', 'be', 'colder', 'than', 'today', 'morning', 'in', 'Tustin'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'tomorrow', 'in', 'Pasadena'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'yesterday', 'be', 'hotter', 'than', 'today', 'in', 'Pasadena'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'tomorrow', 'be', 'hotter', 'than', 'today', 'in', 'Irvine'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['will', 'today', 'be', 'hotter', 'than', 'yesterday', 'in', 'Irvine'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()

    T, P = CYKParse.CYKParse(['what', 'was', 'the', 'temperature', 'in', 'Irvine', 'yesterday'], CYKParse.getGrammarWeatherCustomLocations(locations))
    sentenceTree = getSentenceParse(T)
    updateRequestInfo(sentenceTree)
    reply()
    '''






if __name__ == "__main__":
    main()
