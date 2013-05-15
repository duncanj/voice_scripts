import datetime
import urllib2

def substringBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
		
def toLines(s):
	return s.split('\n')

def findLineWith(lines, s):
	index = -1
	for line in lines:
		index += 1
		if( line.find(s) > -1 ):
			return index
	return -1
	

url = 'http://www.knebworthhouse.com/visit/calendar.html'
s = urllib2.urlopen(url).read()

now = datetime.datetime.now()
month = now.strftime("%B").upper()

wholeMonthCalendar = substringBetween(s, '>'+month+'</span>', '</table>')
lines = toLines(wholeMonthCalendar)
index = findLineWith(lines, '>'+str(now.day)+'</span>')
line = lines[index-2]

openToday = ( line.find("bgcolor") > -1 )

index = findLineWith(lines, '>'+str(now.day+1)+'</span>')
line = lines[index-2]

openTomorrow = ( line.find("bgcolor") > -1 )

response = "Knebworth House is "
response += "open" if openToday else "closed"
response += " today, "
response += "and" if (openToday == openTomorrow) else "but"
response += " "
response += "open" if openTomorrow else "closed"
response += " tomorrow."

print response