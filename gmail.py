import urllib2
 
USERNAME = ''
PASSWORD = ''
FEED_URL = 'https://mail.google.com/mail/feed/atom'
 
def get_unread_msgs(user, passwd):
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(
        realm='New mail feed',
        uri='https://mail.google.com',
        user='{user}@gmail.com'.format(user=user),
        passwd=passwd
    )
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    feed = urllib2.urlopen(FEED_URL)
    return feed.read()

def substringBetween( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

 
##########
 
if __name__ == "__main__":
    import getpass
 
    user = USERNAME
    #passwd = getpass.getpass('Password: ')
    passwd = PASSWORD
    xml = get_unread_msgs(user, passwd)
    fullcount = substringBetween(xml, '<fullcount>', '</fullcount>')

    n = int(fullcount)
    
    if n == 0:
        print 'You have no unread messages.'
    elif n == 1:
        print 'You have 1 unread message.'
    else:
        print 'You have '+fullcount+' unread messages.'
 
    if n > 0:
        entries = xml.split('<entry>')
        index = 0
        for entry in entries:
            if index > 0:
                title = substringBetween(entry, '<title>', '</title>')
                authorBlock = substringBetween(entry, '<author>', '</author>')
                authorName = substringBetween(authorBlock, '<name>', '</name>')
                print 'Email '+str(index)+'. From ' +authorName+', with subject, ' + title
            index = index + 1
    print 'End of messages.'

#    print xml
