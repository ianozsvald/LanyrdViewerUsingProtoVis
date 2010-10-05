import cPickle
import os
import time
import twitter # http://mike.verdone.ca/twitter/ v1.4.2

"""Reads lanyrd_attendees.pickle (generated using get_lanyrd_data.py)
   and gets the friends of each screen_name from Twitter's API,
   stores result in attendee_friends.pickle"""

# NOTE you might run out of Twitter API queries - just re-run this script
# when your API limit has reset, it'll pick-up from where it last stopped

# get the list of lanyrd attendees
# load [(screen_name, title, img_url),...]
attendees = cPickle.load(file('lanyrd_attendees.pickle', 'rb'))

tw = twitter.Twitter() # anonymous usage of Twipper API
def get_friends_by_screen_name(screen_name):
    """Get list of friends (by screen_name) for this screen_name"""    
    cursor = -1
    result = []
    while True:
        print "FRIENDS searching for", screen_name, cursor
        res = tw.statuses.friends(screen_name = screen_name, cursor = cursor)
        print "FOUND", 
        result += res['users']
        cursor = res['next_cursor']
        if cursor == 0:
            break
    return result

def get_api_calls_left():
    res = tw.account.rate_limit_status()
    #{'hourly_limit': 150,
    # 'remaining_hits': 0,
    # 'reset_time': 'Tue Sep 28 15:33:30 +0000 2010',
    # 'reset_time_in_seconds': 1285688010}
    return (res['remaining_hits'], res['reset_time_in_seconds'])


# build a pickle of user details
attendee_friends_filename = 'attendee_friends.pickle'
if os.path.exists(attendee_friends_filename):
    attendee_friends = cPickle.load(file(attendee_friends_filename, 'rb'))
    print "Loaded %d attendee_friends" % (len(attendee_friends.keys()))
else:
    print "Making empty attendee_friends"
    attendee_friends = {}

# for each attendee get their twitter friends (if we don't already have them)
for screen_name_nbr, (screen_name, title, img_url) in enumerate(attendees):
    if screen_name in attendee_friends:
        print "Already got", screen_name
    else:
        print "Getting", screen_name, screen_name_nbr, 'of', len(attendees)
        # get full JSON dict reply from twitter for each follower
        friends = get_friends_by_screen_name(screen_name)
        attendee_friends[screen_name] = friends
        cPickle.dump(attendee_friends, file(attendee_friends_filename, 'wb'), protocol = 2)
        remaining_api_hits, reset_time_in_seconds = get_api_calls_left()
        print "Getting tweets for", screen_name, " - API calls left:", remaining_api_hits, " which resets in", int((reset_time_in_seconds - time.time())/60.0), "mins"

        

