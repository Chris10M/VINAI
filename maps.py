import googlemaps
from datetime import datetime
from gps_coordinates import get_coordinates
import re


def init_current_location_():
    import subprocess
    import os

    filename = 'current_location.txt'

    if os.path.exists(filename):
        os.remove(filename)

    subprocess.call(['bash ./get_location.sh'])


#class init__:
#    init_current_location_()


def convert_coordinates(latitude, longitude):
    return dict(zip(['lat', 'lng'], (float(latitude), float(longitude))))


def get_current_location():
    current_location = None
    with open(file='current_location.txt', mode='r') as current_location_file:
        for row in current_location_file:
            current_location = row
            break

    latitude, longitude = current_location.split(',')
    return convert_coordinates(latitude=latitude, longitude=longitude)

class Index:
    nearest = 0
    result = 'results'
    name = 'name'
    address = 'formatted_address'
    geometry = 'geometry'
    location = 'location'
    longitude = 'lng'
    latitude = 'lat'
    best_match = 0
    types = 'types'
    address_components = 'address_components'
    long_name = 'long_name'
    legs = 'legs'
    way = 'html_instructions'
    steps = 'steps'

class Place:
    def __init__(self, name, longitude, latitude, address, type_):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.type = type_
        self.address = address

    def get_address(self):
        return self.address

    def get_location(self):
        return self.latitude, self.longitude

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name


class Map:
    gmaps = googlemaps.Client(key='AIzaSyB35F6NYIY8k0ncFhZlUSzACPXojEtfOw0')
    current_location = get_current_location()
    remove_html_pattern = re.compile(r'(\<.*?\>|\<\/.*\>)')

    @staticmethod
    def where_am_i():
        reverse_geocode_result = Map.gmaps.reverse_geocode(Map.current_location)
        reverse_geocode_result = reverse_geocode_result[Index.nearest][Index.address_components]

        address_list = []

        for address in reverse_geocode_result:
            address_list.append(address[Index.long_name])

        def f7(seq):
            seen = set()
            seen_add = seen.add
            return [x for x in seq if not (x in seen or seen_add(x))]

        address_list = f7(address_list)

        return address_list

    @staticmethod
    def get_nearest_bus_stop():
        now = datetime.now()

        place_result = Map.gmaps.places(query='bus stop', location=Map.current_location)

        place = place_result[Index.result][Index.nearest]

        nearest_bus_stop = \
            Place(name=place[Index.name],
                  longitude=place[Index.geometry][Index.location][Index.longitude],
                  latitude=place[Index.geometry][Index.location][Index.latitude],
                  address=place[Index.address],
                  type_=place[Index.types][Index.best_match])

        directions_result = Map.gmaps.directions(Map.current_location,
                                             nearest_bus_stop.get_location(),
                                             mode="walking",
                                             departure_time=now)

        steps = directions_result[Index.nearest][Index.legs]

        steps = steps[Index.nearest]
        steps = steps[Index.steps]

        way = []

        for step in steps:
            step = step[Index.way]
            for remove in Map.remove_html_pattern.findall(step):
                step = step.replace(remove, '')
            way.append(step)

        return nearest_bus_stop.name, way

    @staticmethod
    def get_to_place(place_to_go):
        now = datetime.now()

        place_result = Map.gmaps.places(query=place_to_go, location=Map.current_location)

        place = place_result[Index.result][Index.nearest]

        place_best_match = \
            Place(name=place[Index.name],
                  longitude=place[Index.geometry][Index.location][Index.longitude],
                  latitude=place[Index.geometry][Index.location][Index.latitude],
                  address=place[Index.address],
                  type_=place[Index.types][Index.best_match])

        directions_result = Map.gmaps.directions(Map.current_location,
                                                 place_best_match.get_location(),
                                                 mode="transit",
                                                 departure_time=now,
                                                 transit_mode='bus')

        steps = directions_result[Index.nearest][Index.legs]

        steps = steps[Index.nearest]
        steps = steps[Index.steps]

        way = []

        for step in steps:
            step = step[Index.way]
            for remove in Map.remove_html_pattern.findall(step):
                step = step.replace(remove, '')
            way.append(step)

        return place_best_match.name, way


if __name__ == '__main__':
    print(Map.where_am_i())
