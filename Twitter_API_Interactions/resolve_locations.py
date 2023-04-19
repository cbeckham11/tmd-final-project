import requests
import json
import time
import csv
import concurrent.futures

def create_url(location):
    fields = "name%2Cgeometry"
    apikey = "AIzaSyBXMZMImjaIqQ9MCuke9KL0jF8UYAMWTLE"
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields={}&key={}".format(location, fields, apikey)
    return url.strip()


def connect_to_endpoint(url):
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    locations = open("non_null_locations_encoded.txt", "r")
    data = locations.read()
    data_into_list = data.split('\n')

    results = []
    for i, location in enumerate(data_into_list):
        url = create_url(location)

        json_response = connect_to_endpoint(url)
        json_object = json.dumps(json_response, indent=4, sort_keys=True)

        data = json.loads(json_object)
        print(data["status"])
        if (data["status"] == "OK"):
            lat = data["candidates"][0]["geometry"]["location"]["lat"]
            lon = data["candidates"][0]["geometry"]["location"]["lng"]
            name = data["candidates"][0]["name"]
            results.append((i, lat, lon, name))
        else:
            lat = None
            lon = None
            name = None
            results.append((i, lat, lon, name))

    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['i', 'lat', 'lon', 'name'])
        for i, lat, lon, name in results:
            writer.writerow([i, lat, lon, name])

    locations.close()


if __name__ == "__main__":
    main()