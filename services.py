from classes import CityObject, TimeZone
from settings import MAX_AMOUNT_OF_CITY_NAMES_FOR_AUTOFILL
from urllib import parse
from typing import Union

__city_object_list = []
__time_zones = []


def parse_timezones(filename: str = 'timeZones.txt'):
    """Parses timezone data from file"""

    with open(filename, encoding='UTF-8') as file:
        list_of_timezones_lists = file.read().split('\n')
        # pop description
        list_of_timezones_lists.pop(0)
        global __time_zones
        for list_ in list_of_timezones_lists:
            if list_ != '':
                tmp = list_.split('\t')
                __time_zones.append(TimeZone(tmp[1], tmp[2]))


def parse_file(filename: str = 'RU.txt'):
    """Parses txt data file, storing all data in a list of CityObjects"""

    with open(filename, encoding='UTF-8') as file:
        list_of_data_lists = file.read().split('\n')
        global __city_object_list
        for list_ in list_of_data_lists:
            if list_ != '':
                __city_object_list.append(CityObject(list_.split('\t')))


def parse_request(unparsed_request: str = 'https://host/get_city_by_id') -> Union[str, tuple]:
    """Parses request line, getting requested method and parameters out of the line"""

    method, request, error = None, None, None

    if unparsed_request.find('/get_city_by_id/') == 0:
        method = '/get_city_by_id/'
        try:
            city_id = int(unparsed_request.replace('/get_city_by_id/', ''))
        except ValueError:
            error = {'Code': 400, 'Description': 'Bad Request'}
        else:
            request = {'city_id': city_id}

    elif unparsed_request.find('/load_page/') == 0:
        method = '/load_page/'
        try:
            page_number, cities_per_page_amount = list(map(int, unparsed_request.replace(method, '').split('&')))
        except ValueError:
            error = {'Code': 400, 'Description': 'Bad Request'}
        else:
            request = {'page_number': page_number, 'cities_per_page_amount': cities_per_page_amount}

    elif unparsed_request.find('/compare/') == 0:
        method = '/compare/'
        try:
            city1, city2 = unparsed_request.replace(method, '').split('&')
        except ValueError:
            error = {'Code': 400, 'Description': 'Bad Request'}
        else:
            request = {'city1': city1, 'city2': city2}

    elif unparsed_request.find('/autofill/') == 0:
        method = '/autofill/'
        incomplete_city_name = unparsed_request.replace(method, '')
        request = ({'incomplete_city_name': incomplete_city_name})
    else:
        error = {'Code': 405, 'Description': 'Method Not Allowed'}

    return method, request, error


def handle_request(unparsed_request) -> tuple:
    """Handles requests, received from server request handler"""

    response, error = None, None
    unquoted_request = parse.unquote_plus(unparsed_request, encoding="UTF-8")
    method, request, error = parse_request(unquoted_request)
    if error is None:
        if method == '/get_city_by_id/':
            response, error = handle_get_city_by_id(request)
        elif method == '/load_page/':
            response = handle_load_page(request)
        elif method == '/compare/':
            response, error = handle_compare(request)
        elif method == '/autofill/':
            response, error = handle_autofill(request)
    return response, error


def handle_get_city_by_id(request: tuple) -> tuple:
    """Handles get_city_by_id method"""

    response, error = None, None
    try:
        city_object = next(x for x in __city_object_list if x.geonameid == str(request['city_id']))
    except StopIteration:
        error = {'Code': 404, 'Description': 'City not found'}
    else:
        response = city_object.__dict__
    return response, error


def handle_load_page(request: tuple) -> str:
    """Handles load_page method"""

    i = 1
    displayed_cities = __city_object_list[request['page_number']*request['cities_per_page_amount']:
                                          request['page_number']*request['cities_per_page_amount']
                                          + request['cities_per_page_amount']]
    response = '{'
    for city_object in displayed_cities:
        response += f'"City №{i}": {city_object.__dict__}, '
        i += 1
    response += '}'
    return response


def handle_compare(request: tuple) -> tuple:
    """Handles compare method"""

    response, error = None, None
    try:
        city1_object = find_city_by_name(request['city1'])
        city2_object = find_city_by_name(request['city2'])
    except ValueError:
        error = {'Code': 404, 'Description': 'City not found'}
        return response, error

    response = {}
    if city1_object.longitude > city2_object.longitude:
        longitude_cmp = {'North_most_city': request['city1']}
    elif city1_object.longitude < city2_object.longitude:
        longitude_cmp = {'North_most_city': request['city2']}
    else:
        longitude_cmp = {'North_most_city': 'Both on the same longitude'}
    response.update(longitude_cmp)

    if city1_object.timezone == city2_object.timezone:
        timezone_cmp = {'timezone_difference': '0.0'}
    else:
        city1_gmt_offset = float((next(x for x in __time_zones if x.time_zone_id == city1_object.timezone)).gmt_offset)
        city2_gmt_offset = float((next(x for x in __time_zones if x.time_zone_id == city2_object.timezone)).gmt_offset)
        timezone_cmp = {'timezone_difference': str(abs(city1_gmt_offset - city2_gmt_offset))}
    response.update(timezone_cmp)
    response.update({'City №1': city1_object.__dict__})
    response.update({'City №2': city2_object.__dict__})
    return response, error


def handle_autofill(request: tuple) -> tuple:
    """Handles autofill method"""

    response, error = None, None
    most_similar_city_list = []
    for city_object in __city_object_list:
        for city_name in get_all_city_names(city_object):
            if city_name.find(request['incomplete_city_name']) != -1 and city_name not in most_similar_city_list:
                most_similar_city_list.append(city_name)
        if len(most_similar_city_list) == MAX_AMOUNT_OF_CITY_NAMES_FOR_AUTOFILL:
            break

    if len(most_similar_city_list) == 0:
        error = {'Code': 404, 'Description': 'Similarities not found'}
    most_similar_city_list = most_similar_city_list[:MAX_AMOUNT_OF_CITY_NAMES_FOR_AUTOFILL]
    response = {'most_similar_cities': most_similar_city_list}
    return response, error


def get_all_city_names(city_object: object) -> list:
    """Puts all possible names of city_object to list"""

    name_list = city_object.alternatenames.split(',')
    name_list.append(city_object.name)
    name_list.append(city_object.asciiname)
    # remove repeats
    name_list = list(set(name_list))
    return name_list


def find_city_by_name(name: str) -> object:
    """Finds all occurrences of the city name in __city_object_list, returns the one with biggest population"""

    suitable_city_positions_list = [i for i, x in enumerate(__city_object_list) if name in get_all_city_names(x)]

    if len(suitable_city_positions_list) == 0:
        raise ValueError
    elif len(suitable_city_positions_list) == 1:
        city_object = __city_object_list[suitable_city_positions_list[0]]
    else:
        city_object = __city_object_list[suitable_city_positions_list.pop()]
        for pos in suitable_city_positions_list:
            if int(__city_object_list[pos].population) > int(city_object.population):
                city_object = __city_object_list[pos]
    return city_object
