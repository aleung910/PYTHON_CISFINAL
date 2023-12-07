from underground import SubwayFeed
import datetime
import json 
import pprint

url = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct/gtfs-bdfm"
API_KEY = 'Sk9HMgyQuN24slsbgXEEs2avCkx5pbxr68SxonnD'

ROUTES = ["1","2","3","4","5","6"]

for route in ROUTES[::]:
  feed = SubwayFeed.get(route, api_key=API_KEY)
  for train, val in feed.extract_stop_dict().items():
    pass

with open('stopsID.json', 'r') as f:
  stopsID = json.load(f)

with open('stations.json', 'r') as f:
  stations = json.load(f)

with open('lines.json', 'r') as f:
  lines = json.load(f)

def build_graph():
  graph = {}

  for key, stops in lines.items():

    for index in range(len(stops) - 1):
      if stops[index] in graph:
        graph[stops[index]].update({ stops[index + 1]: 1})
      else:
        graph[stops[index]] = {}
  
  for key, stops in lines.items():

    for index in range(len(stops) - 1)[::-1]:
      if stops[index] in graph:
        graph[stops[index]].update({ stops[index - 1]: 1})
      else:
        graph[stops[index]] = {}
        
  return graph

def graph_weight(graph):
  stopTimes = {}
  for route in ROUTES[:6:]:
    feed = SubwayFeed.get(route, api_key=API_KEY)
    print(len(stopTimes))
    for train, val in feed.extract_stop_dict().items(): 
      for x, y in val.items(): 
        if x in stopsID:    # Checks if x=(station ID API gives) is in the JSON
          stopTimes[stopsID[x]] = y[0] # Makes the stop the key, and the list of times the value
                                    # ex. "{175th st: [time1, time2, time3 ...] }"  
  pprint.pprint(stopTimes) 
   
  for key, stops in graph.items():
    for stop, weight in stops.items():
      if stop in stopTimes:
        stops[stop] = stopTimes[stop]

  return graph

def check_MTA_data():
  for key, val in feed.extract_stop_dict().items():
    print("-" * 100)
    print(key) # Train
    for x, y in val.items(): 
      print()
      print(x) # Gets the ID of stop
      if x in stopsID:
        print(stopsID[x]) # Get the name of Stop
        print()
        for val in y:
          print(val) # Time of the upcoming stops
    break

# # Get the start location time
# # Go to the next stop latest time
# # subtract the start time and last stop time
# # total_time = start_time - nextstop_time 
# # return total_time

def amount_of_time(start, end):
    start_time = None

    for train, stops in feed.extract_stop_dict().items():
        for stop, times in stops.items():
            if stop in stopsID:
                try:
                    # Check if the current stop is the starting station
                    if stopsID[stop] == start:
                        time = str(times[0])
                        start_time = datetime.datetime(int(time[:4]), int(time[5:7]), int(time[8:10]),
                                                       int(time[11:13]), int(time[14:16]), int(time[17:19]))

                    # Check if the current stop is the destination station
                    elif stopsID[stop] == end and start_time:
                        time = str(times[0])
                        next_stop_time = datetime.datetime(int(time[:4]), int(time[5:7]), int(time[8:10]),
                                                            int(time[11:13]), int(time[14:16]), int(time[17:19]))
                        
                        # Calculate the time difference
                        travel_time = next_stop_time - start_time
                        return travel_time
                        
                except KeyError as e:
                    print("KeyError:", e)

    return -1


def subtract_datetime(first, second):
  first = str(first)
  second = str(second)
  start_time = datetime.datetime(int(first[:4]), int(first[5:7]), int(first[8:10]), int(first[11:13]), int(first[14:16]), int(first[17:19]))
  nextstop_time = datetime.datetime(int(second[:4]), int(second[5:7]), int(second[8:10]), int(second[11:13]), int(second[14:16]), int(second[17:19]))
  return nextstop_time - start_time


# Take into account North and South
# Only works for one train
# Have to implement a way to check transfers

# with open("graph.json", "w") as outfile: 
#     json.dump(build_graph(), outfile)*ru
# check_MTA_data()
pprint.pprint(build_graph())

#test for A train
# print(amount_of_time("Inwood-207 St","145 St"))
# print(amount_of_time("145 St", "Inwood-207 St"))



# print(amount_of_time("145 St","190 St"))
# print(amount_of_time("190 St", "145 St"))


# # Inwood - 207 St for jso, INWOOD RIGHT NOW IS GOOOD I NEED TO COPY THAT PATTERN

# print(amount_of_time("Kingsbridge Rd","170 St"))
# print(amount_of_time("170 St","Kingsbridge Rd"))

#BTRAIN TEST
# print(amount_of_time("170 St","167 St")) #numbers work for B
# print(amount_of_time("W 4 St-Wash Sq","42 St-Bryant Pk")) 


# # 168 St-Washington Hts

#CTRAIN TEST
# print(amount_of_time("Fordham Rd","Coney Island-Stillwell Av")) #numbers work for B
