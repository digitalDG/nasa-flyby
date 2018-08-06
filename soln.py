import json
import datetime
import requests
from pprint import pprint

# constants within the module. Defined for ease of use
API_KEY = "9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute"
BASE_URI = "https://api.nasa.gov/planetary/earth/assets"

def flyby(latitude, longitude):
    
    """
    Sends HTTP GET request to NASA API to predict the next time a satellite image will
    be taken from a specified location based on latitude and longitude coordinates.
    """
    
    # check the input parameters for valid latitude
    if latitude > 90 or latitude < -90: 
        print('ERROR: Please input valid latitude {}. The valid latitude ranges: -90 to 90 '.format(latitude))
        return
    
    # check the input parameters for valid longitude
    if longitude > 180 or longitude < -180:
        print('ERROR: Please input valid longitude {}. The valid longitude ranges: -180 to 180 '.format(longitude))
        return

    # define query args to the API
    query_args = { 
        "lon" : longitude,
        "lat": latitude,
        "api_key": API_KEY 
    }
    
    # try/catch in order to catch any exceptions generated in request i.e. connection errors, timeouts  
    try:
        r = requests.get(BASE_URI, params=query_args)
        r.raise_for_status()
        
        print("Retreiving data from {}".format(r.url))
    
        # print(r.text)
    
        # make sure some data was returned
        if r.text:

            # make sure json data is deserialized correctly
            try:
                # get the data from the  GET request
                data = r.json()
            except ValueError:
                # no JSON returned
                print('ERROR: Unable to parse JSON data')
                return

            # debugging dump of json data
            # print(json.dumps(data, indent=4))
            # pprint(data)


            # make sure a empty response was not returned when translate to json
            if data:
                if data['count'] < 2:
                    print('ERROR: Not enough data points to calculate next date')
                    return

                # parse dates to datetime dates
                dates = [datetime.datetime.strptime(i['date'], '%Y-%m-%dT%H:%M:%S') for i in data['results']]

                # sort the dates so they are in order
                dates.sort()

                # compute times between each image
                deltas = [(dates[i + 1] - dates[i]) for i in range(0, len(dates) - 1)]

                # compute average of time between every image 
                avg_time_delta = sum(deltas, datetime.timedelta()) / len(deltas)

                # debugging
                print('Average time delta: {}'.format(avg_time_delta))

                # Calculate next time by taking last date added to the avg time delta
                next_time = str(dates[len(dates)-1] + avg_time_delta)

                # print out the next time (on average) an image should be recorded
                print('Next time: {}'.format(next_time))
        else :
            # if we got here then no data exists from the http request
            print('No data exists for specified location')

        
    except requests.exceptions.HTTPError as errh:
        # This will catch http type errors i.e 404
        print ("Http Error:",errh)
        return
    except requests.exceptions.ConnectionError as errc:
        # connection errors
        print ("Error Connecting:",errc)
        return
    except requests.exceptions.Timeout as errt:
        # timeout errors
        print ("Timeout Error:",errt)
        return
    except requests.exceptions.RequestException as e: 
        # generic request errors
        print(e)
        return
    
    


print('Test 1')
flyby(90, 180)

print()

print('Testing invalid latitude coordinates')
flyby(-91, -79.34234)

print()

print('Testing invalid longitude coordinates')
flyby(-90, -181)

print()

#
#     Fun location           Latitude    Longitude
#     ---------------------  ----------  ------------
#     Grand Canyon           36.098592   -112.097796
#     Niagra Falls           43.078154   -79.075891
#     Four Corners Monument  36.998979   -109.045183
#     Delphix San Francisco  37.7937007  -122.4039064
# 

print('Testing Grand Canyon ')
flyby(36.098592, -112.097796)

print()

print('Testing Niagra Falls')
flyby(43.078154, -79.075891)

print()

print('Testing Four Corners Monument')
flyby(36.998979,-109.045183)

print()

print('Testing Delphix SF')
flyby(37.7937007,-122.4039064)

    