import json
import csv
from geopy import distance

def get_closest_mrt(coord, year, mrt_stations):
    open_stations = mrt_stations[year]
    min_dist = float('inf')
    closest_station = None
    for station in open_stations:
        station_name = station[0]
        station_coord = (station[1], station[2])
        dist = distance.distance(coord, station_coord).km
        if dist < min_dist:
            closest_station = station_name
            min_dist = dist
    return (closest_station, round(min_dist, 3))



path = "/Users/tanayrishi/Downloads/"

f = open(path + "mrt.json")

data = json.load(f)
#print(data)
#print(len(data))
open_year = {}
for y in range(1990, 2024):
    open_year[y] = []
for st in data:
    date = data[st][0]
    if date:
        try:
            year = int(date[0:4])
        except:
            year = date
            #print(year, st, "wrong format")
            #print(st)
            continue
    else:
        #print(st, "no date")
        continue
    lat = data[st][1]
    longi = data[st][2]
    
    for oy in open_year:
        if year <= oy:
            open_year[oy].append([st, lat, longi])

seen_distances = {}

with open(path + 'all_housing.csv', 'r') as houses, open(path + 'housing_with_distance_to_mrt.csv', 'w') as outfile:
    freader = csv.reader(houses)
    fwriter = csv.writer(outfile)
    header = next(freader, None)
    header.append('nearest_station')
    header.append('distance_to_nearest_station')
    fwriter.writerow(header)
    print(header)
    count = 0
    for row in freader:
        row[11] = row[11].strip()
        block = row[0] + " " + row[1]
        sale_year = int(row[6])
        location = (float(row[12]), float(row[13]))
        if block in seen_distances:
            if sale_year in seen_distances[block]:
                nearest_station = seen_distances[block][sale_year]
            else:
                nearest_station = get_closest_mrt(location, sale_year, open_year)
                seen_distances[block][sale_year] = nearest_station
        else:
            nearest_station = get_closest_mrt(location, sale_year, open_year)
            seen_distances[block] = {}
            seen_distances[block][sale_year] = nearest_station
        row.append(nearest_station[0])
        row.append(nearest_station[1])
        fwriter.writerow(row)
        count += 1
        if count % 100000 == 0:
            print(count)
        
        
        
print(count)
        
    


