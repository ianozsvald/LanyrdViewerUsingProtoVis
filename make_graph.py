import cPickle
import simplejson as json

"""Load lanyrd_attendees.pickle and attendee_friends.pickle, build a 
   graph (nodes and edges) of people at the event and their attending friends
   which can then be exported as a lump of JSON for visualisation"""

# load [(screen_name, title, img_url),...]
attendees = cPickle.load(file('lanyrd_attendees.pickle', 'rb'))

# load {screen_name: twitter friend detials, ...}
attendee_friends_filename = 'attendee_friends.pickle'
attendee_friends = cPickle.load(file(attendee_friends_filename, 'rb'))

# make set of all attendees
attendees_screen_names = [screen_name for screen_name, title, img_url in attendees]
attendees_set = set(attendees_screen_names)
print "Working with %d attendees" % (len(attendees_set))

# friends at this event {screen_name:[friend_screen_names, ...], ...}
friends_at_event = {}

# iterate over all attendees
for screen_name, title, img_url in attendees:
    #print screen_name
    friends_screen_names = []
    for items in attendee_friends[screen_name]:
        friends_screen_names.append(items['screen_name'])
    friends_screen_names_set = set(friends_screen_names)
    friends_at_event[screen_name] = friends_screen_names_set.intersection(attendees_set)

# build node list, node_ids would be 0..len(nodes)-1
# base this on Kyran's example:
#var miserables = {
# nodes:[
#   {nodeName:"Myriel", group:1},
#   {nodeName:"Napoleon", group:1},
#   {nodeName:"Mlle. Baptistine", group:1},
#   {nodeName:"Mme. Magloire", group:1},
#   {nodeName:"Countess de Lo", group:1},
#   {nodeName:"Geborand", group:1},
#
nodes = []
for screen_name, title, img_url in attendees:
    nodes.append((dict(nodeName=screen_name, group=1, title=title, img_url=img_url)))

# map list of screennames to ids, build dict to lookup id from name e.g.
#{'andybak': 1,
# 'empika': 0,...}
attendee_ids = dict([(s,n) for n,s in enumerate(attendees_screen_names)])

# build links list, based on relationship of myself (at the event) to
# everyone else who is a friend who is at the event
# base this on Kyran's example:
# links:[
#   {source:1, target:0, value:1},
#   {source:2, target:0, value:8},
#   {source:3, target:0, value:10},
#   {source:3, target:2, value:6},
#   {source:4, target:0, value:1},
#   {source:5, target:0, value:1},
#   {source:6, target:0, value:1},
#   {source:7, target:0, value:1},
links = []
for node_id, (screen_name, title, img_url) in enumerate(attendees):
    for friend_screen_name in friends_at_event[screen_name]:
        friend_node_id = attendee_ids[friend_screen_name]
        links.append(dict(source=node_id, target=friend_node_id, value=1))

print "Created %d nodes with %d links" % (len(nodes), len(links))

# create JSON file with nodes and links for ProtoVis visualisations
graph = conf_data=dict(nodes=nodes, links=links)
f = file('graph.js', 'w')
f.write('conf_data = ') # write variable name at the start of the file
json.dump(graph, f, indent=2)
f.close()

print "Graph generated - now copy graph.js into SocialGraphVis and then open lanyard.html in your browser"
