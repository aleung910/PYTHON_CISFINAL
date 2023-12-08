from underground import SubwayFeed
import datetime
import json 
import pprint

url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-bdfm"
API_KEY = 'Sk9HMgyQuN24slsbgXEEs2avCkx5pbxr68SxonnD'
ROUTE = 'A'
ROUTES = ["1","2","3","4","5","6","7","A","B","C","D","E","F","G","J","L","M","N","Q","R","W","Z"]
NUM_OF_ROUTES = 6
feed = SubwayFeed.get(ROUTE, api_key=API_KEY) 

with open('stopsID.json', 'r') as f:
  stopsID = json.load(f)

with open('lines.json', 'r') as f:
  lines = json.load(f)

def build_graph():
  graph = {}
  count = 0
  for key, stops in lines.items():

    for index in range(len(stops) - 1):
      if stops[index] in graph:
        graph[stops[index]][f"S {stops[index + 1]}"] = 1
      else:
        graph[stops[index]] = {f"S {stops[index + 1]}" : 1}
    count += 1
    if count == NUM_OF_ROUTES:
      break

  count = 0
  for key, stops in lines.items():
    for index in range(len(stops))[:0:-1]:
      if stops[index] in graph:
        graph[stops[index]][f"N {stops[index - 1]}"] = 9999999
      else:
        graph[stops[index]] = {f"N {stops[index - 1]}" : 9999999}
    count += 1
    if count == NUM_OF_ROUTES:
      break

  return graph

def graph_weight(graph):
  stopTimes = {}
  for route in ROUTES[:NUM_OF_ROUTES:]:
    feed = SubwayFeed.get(route, api_key=API_KEY)
    for train, val in feed.extract_stop_dict().items(): 
      for x, y in val.items(): 
        if x in stopsID:    # Checks if x=(station ID API gives) is in the JSON
          stopTimes[f"{x[-1]} {stopsID[x]}"] = y # Makes the stop the key, and the list of times the value
                                    # ex. "{N 175th st: [time1, time2, time3 ...] }"  

  for key, stops in graph.items(): # Key = stop, stops = all possible stops key can make 
    for stop, weight in stops.items(): # stop = N 175th
      if f"{stop[0]} {key}" in stopTimes:
        startTime = stopTimes[f"{stop[0]} {key}"][0]
        if stop in stopTimes: # Used to check if name is the same
          endTime = stopTimes[stop][0]
        else:
          print(stop) # IF NOT FIX THESE NAMES!

        stops[stop] = subtract_datetime(startTime, endTime)

  return graph

def check_MTA_data():
  for key, val in feed.extract_stop_dict().items():
    print("-" * 100)
    print(key) # Train ex. "A"
    for x, y in val.items(): 
      print()
      print(x) # Gets the ID of stop
      if x in stopsID:
        print(stopsID[x]) # Get the name of Stop
        print()
        for val in y: # y is a list of times [time1, time2, ...]
          print(val) # Time of the upcoming stops
          break
    break

def subtract_datetime(first, second):
  first = str(first)
  second = str(second)
  start_time = datetime.datetime(int(first[:4]), int(first[5:7]), int(first[8:10]), int(first[11:13]), int(first[14:16]), int(first[17:19]))
  nextstop_time = datetime.datetime(int(second[:4]), int(second[5:7]), int(second[8:10]), int(second[11:13]), int(second[14:16]), int(second[17:19]))
  time_difference = nextstop_time - start_time
  if int(time_difference.total_seconds()) < 0:
    time_difference = start_time - nextstop_time
  return int(time_difference.total_seconds())

# check_MTA_data()
stopGraph = graph_weight(build_graph())
with open("stopsGraph.json", "w") as outfile: 
  json.dump(stopGraph, outfile)
# pprint.pprint(stopGraph)