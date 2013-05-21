import urllib2
import os

def substringBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
		
airport = 'stansted'

url = 'http://ukga.com/airfield/'+airport+'/weather'
s = urllib2.urlopen(url).read()

section = substringBetween(s, '<H2>METAR</H2>', '<h2>')
section = section + '*END*'
section = substringBetween(section, '</pre>', '*END*')

# delete all blank lines from 'section' string
section = os.linesep.join([s.strip() for s in section.splitlines() if s.strip() != ''])

section = section.replace('&deg;',' degrees ') # replace code for degrees with word
section = section.replace('\n',' ')  # replace newlines with spaces
section = section.replace('.','\n')  # replace full stop with line separator

# split into lines, strip whitespace from each one, then reassemble into one string
section = os.linesep.join([s.strip() for s in section.splitlines()])

section = section.replace('Our last available update is from ','This is the metar report for '+airport+' airport at ')

print section
