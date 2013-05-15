import sys
import urllib2

def substringBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

if len(sys.argv) < 2:
    sys.exit('Usage: %s bbc-weather-location-id' % sys.argv[0])

location = sys.argv[1]
#location = "2647044" # from http://www.bbc.co.uk/weather/2647044
url = "http://www.bbc.co.uk/weather/" + location
s = urllib2.urlopen(url).read()
#print response

a = substringBetween(s, '<script id=\"forecast-summary-0\"', '</script>')
first = substringBetween(a, '<p class=\"body\">', '</p>')
firstWhen = substringBetween(a, '<h4 class=\"title\">', '</h4>')
print firstWhen
print first

c = substringBetween(s, '<script id=\"forecast-summary-1\"', '</script>')
second = substringBetween(c, '<p class=\"body\">', '</p>')
secondWhen = substringBetween(c, '<h4 class=\"title\">', '</h4>')
print secondWhen
print second


