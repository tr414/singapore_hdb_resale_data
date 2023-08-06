import googlemaps
import csv
import os
import requests

base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
api_key = 'your-api-key'  #insert your google API key

#sample = {'results': [{'address_components': [{'long_name': '1', 'short_name': '1', 'types': ['street_number']}, {'long_name': 'Beach Road', 'short_name': 'Beach Rd', 'types': ['route']}, {'long_name': 'Downtown Core', 'short_name': 'Downtown Core', 'types': ['neighborhood', 'political']}, {'long_name': 'Singapore', 'short_name': 'Singapore', 'types': ['locality', 'political']}, {'long_name': 'Singapore', 'short_name': 'SG', 'types': ['country', 'political']}, {'long_name': '190001', 'short_name': '190001', 'types': ['postal_code']}], 'formatted_address': '1 Beach Rd, Singapore 190001', 'geometry': {'location': {'lat': 1.2954836, 'lng': 103.8544382}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 1.296576430291502, 'lng': 103.8562065302915}, 'southwest': {'lat': 1.293878469708498, 'lng': 103.8535085697085}}}, 'place_id': 'ChIJN9BtAicZ2jERNySepBAE8y8', 'plus_code': {'compound_code': '7VW3+5Q Singapore', 'global_code': '6PH57VW3+5Q'}, 'types': ['street_address']}], 'status': 'OK'}
#rpath = "/Users/tanayrishi/Downloads/"

path = "path-to-directory-with-raw-data" #insert path to directory which contains the hdb proces csv file
seen_address = {}

with open(path + 'hdb-property-information.csv', 'r', encoding="utf8", errors='ignore') as f, open(path + 'pc.csv', 'w') as outfile:
    freader = csv.reader(f)
    fwriter = csv.writer(outfile)
    header = next(freader, None)
    fwriter.writerow([header[0], header[1], 'postal_code', 'latitude', 'longitude'])
    count = 0
    not_found = 0
    for row in freader:
        params = {
            'address' : "Block {} {}, Singapore".format(row[0],row[1].capitalize()),
            'country' : 'SG',
            'key' : api_key
        }
        #print(params)
        response = requests.get(base_url, params=params)
        results = response.json()['results']
        #results = sample['results']
        
        if len(results) > 0:
            location = results[0]['geometry']['location']
            postal_code = None
            for component in results[0]['address_components']:
                if 'postal_code' in component['types']:
                    postal_code = component['long_name']
                    break
            lat = location['lat']
            lon = location['lng']
            fwriter.writerow([row[0], row[1], postal_code, lat, lon])
        else:
            fwriter.writerow([row[0], row[1], "Null", "Null", "Null"])
            print("No results found")
            not_found += 1
            print(count)
    
        count += 1
        #if count > 0:
        #    break
    print(count, not_found)
    