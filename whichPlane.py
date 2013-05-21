##########################################################################
#
# This script reads data from dump1090, a program that runs as a server and
# provides realtime data read from a cheap USB stick that can receive aircraft
# ADS-B transponder signals.  Google for 'sdr usb dump1090' for more details.
#
# The output from this script is in the form of lines that look like:
#
#   R Y R 8 5 8 5, is 7 kilometers away to the North-East, at 2875 feet and 
#   heading South-West, and is en-route from Rhodes Diagoras, Rhodos, Greece,
#   to London Stansted.
#
#   R Y R 3 E H, is 11 kilometers away to the East, at 2575 feet and heading 
#   East, and is en-route from Tenerife Sur, Tenerife, Spain, to London Stansted.
#
# (the flight numbers are separated by spaces to make them sound right)
#
##########################################################################

# Enter the server name/ip and port that dump1090 is running on
dump1090url = 'http://192.168.1.102:8080'

# Enter the latitude/longitude of where you live.  Note that you might
# wish to reduce the precision before committing any changes to github.
ourLatitude = 51.8
ourLongitude = -0.08

# Aircraft have to be within this distance to count
distanceLimit = 15.0

###########################################################################


import urllib2
import os
import json
from math import radians, degrees, cos, sin, asin, sqrt, atan2


# taken from http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def bearing(lon1, lat1, lon2, lat2):
    """
    Calculate the bearing between two points on the earth.
    """
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    
    diffLong = radians(lon2 - lon1)

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

    bearing = atan2(x, y)

    bearing = degrees(bearing)
    result = (bearing + 360) % 360

    return result

def bearingToWords(bearing):
    index = int((bearing + 22.5)/45.0) % 8
    words = ['North','North-East','East','South-East','South','South-West','West','North-West']
    return words[index]


def substringBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def unique(items):
    found = set([])
    keep = []

    for item in items:
        if item not in found:
            found.add(item)
            keep.append(item)

    return keep

def formatAirport(area, airport):
    pos = airport.find(' (')
    result = airport[:pos] # strip off the ICAO code for the airport - e.g. (LHR)

    result = result + ', ' + area
    result = result.replace(', United Kingdom', '') # we know where these airport are; no need to tell us the country

    # turn "Stansted, London" into "London Stansted"
    if result.endswith(', London'):
        pos = result.find(', London')
        result = result[:pos]
        result = 'London '+result

    # remove any duplicates, so we don't get 'Birmingham, Birmingham'
    result = ', '.join(unique([s.strip() for s in result.split(',')]))

   
#    print 'converting from |'+area+'| and |'+airport+'| to |'+result+'|'
    return result

# begin script

url = dump1090url + '/data.json'
s = urllib2.urlopen(url).read()  # read all text (it's in json format)
j = json.loads(s)

for plane in j:
    dist = haversine(ourLongitude, ourLatitude, plane['lon'], plane['lat'])
    b = bearing(ourLongitude, ourLatitude, plane['lon'], plane['lat'])
    plane['dist'] = dist  # update this plane's dictionary/map with the dist
    plane['bearing'] = b  # and the bearing

# sort the list of dictionaries/maps by their 'dist' value
sortedByDistance = sorted(j, key=lambda k: k['dist'])

planes = 0

for i in [0,1]:
    if len(sortedByDistance) > i:
        p = sortedByDistance[i]
        if p['dist'] < distanceLimit:
            # get more information
            moredata = urllib2.urlopen('http://planefinder.net/endpoints/planeData.php?adshex='+p['hex']+'&isFAA=0&ts=1').read()
            moredata = moredata.splitlines()[2] # first 2 lines are warning msg
            j2 = json.loads(moredata)
            route = j2["route"].split(' to ') # XYZ to ABC
            if route and str(route) != 'N/A':
                fromArea = substringBetween(route[0],'title="','"')
                fromAirport = substringBetween(route[0],'>','<')
                toArea = substringBetween(route[1],'title="','"')
                toAirport = substringBetween(route[1],'>','<')

                p['from'] = formatAirport(fromArea, fromAirport)
                p['to'] = formatAirport(toArea, toAirport)
            
            flight = ' '.join(p['flight'].strip())
            dist = str(int(round(p['dist'])))
            out = flight + ', is ' + dist + ' kilometers away to the ' + bearingToWords(p['bearing'])+ ', at ' + str(p['altitude']) + ' feet and heading ' + bearingToWords(p['track'])
            if p['from'] and p['to']:
                out = out + ', and is en-route from '+p['from']+', to '+p['to']
            out = out + '.'
            print out
            planes = planes + 1

if planes == 0:
    print 'There are no commercial aircraft in the vicinity.'
