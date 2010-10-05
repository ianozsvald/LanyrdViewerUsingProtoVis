import urllib2
import re
import cPickle

"""Reads Lanyrd event page to get attendees at an event,
   writes out lanyrd_attendees.pickle with their screen names"""

# Get list of attendees from Lanyrd.com for an event...
# William Gibson's event is lightly populated at Lanyrd, makes for a good test case
URL = "http://lanyrd.com/2010/intelligence-squared-with-william-gibson/"
# note for Gibson page ignore the Trackers warning message
# BarCamp had about 60 attendees, Flash on the Beach about 100
#URL = "http://lanyrd.com/2010/barcamp-brighton/"
#URL = "http://lanyrd.com/2010/fotb/"

lines = urllib2.urlopen(URL).readlines()
items = []
attending = False
for line in lines:
    # simple test to get data only from Attendees list
    if line.find("<h2>Attendees (") > -1:
        attending = True
        #print "Found attending"
    if line.find("<h2>Trackers (") > -1:
        attending = False
        #print "Found tracking"

    # only look for attendees if we're in the Attending block
    if attending:
        line = line.strip('\t')
        if line.startswith('<li><a href="/people'):
            screen_name, title, img_url = re.findall('<li><a href="/people/(.*?)/" title="(.*?)" class="avatar-med"><img src="(.*?)"', line)[0]
            # turn 'Richard Willis - @richtextformat' -> 'Richard Willis'
            title = title.split('-')[0].strip()
            items.append((screen_name, title, img_url))

if attending == True:
    print "WARNING: attending should be False (but it is True) - does 'Trackers (xxx)' exist on website?"
    # this might not be a bug but it might indicate that the marker 'Trackers (xxx)' doesn't
    # exist on lanyrd's page any more - possibly the html got renamed (it has happened once already)?
    # note all events have Trackers though, it is a convenient marker whilst they're changing their mark-up though

print "Get %d lanyrd attendees for %s" % (len(items), URL)
cPickle.dump(items, file('lanyrd_attendees.pickle', 'wb'), protocol = 2)
