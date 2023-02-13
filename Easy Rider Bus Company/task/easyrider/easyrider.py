# Write your code here
import json
import re

STOP_TYPE = ['S', 'O', 'F']
STOP_NAME_SUFFIX = ['Road', 'Avenue', 'Boulevard', 'Street']

errors = {
    "bus_id": 0,
    "stop_id": 0,
    "stop_name": 0,
    "next_stop": 0,
    "stop_type": 0,
    "a_time": 0,
}

json_str = input()
# json_str = '''
# [
#     {
#         "bus_id": 128,
#         "stop_id": 1,
#         "stop_name": "Prospekt Avenue",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": "08:12"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 5,
#         "stop_type": "",
#         "a_time": "08:19"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 5,
#         "stop_name": "Fifth Avenue",
#         "next_stop": 7,
#         "stop_type": "O",
#         "a_time": "08:25"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:37"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 2,
#         "stop_name": "Pilotow Street",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": "09:20"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 6,
#         "stop_type": "",
#         "a_time": "09:45"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 7,
#         "stop_type": "",
#         "a_time": "09:59"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "10:12"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 4,
#         "stop_name": "Bourbon Street",
#         "next_stop": 6,
#         "stop_type": "S",
#         "a_time": "08:13"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:16"
#     }
# ]
# '''


def check_name(name):
    re_tmpl = rf'^[A-Z][\w ]+({"|".join(STOP_NAME_SUFFIX)})$'
    return re.match(re_tmpl, str(name)) is not None


def check_time(time):
    re_tmpl = r'^(0\d|1\d|2[0-3]):[0-5]\d$'
    return re.match(re_tmpl, str(time)) is not None


def check_json_data(json_obj):
    for item in json_obj:
        if type(item['bus_id']) is not int:
            errors['bus_id'] += 1
        if type(item['stop_id']) is not int:
            errors['stop_id'] += 1
        if type(item['next_stop']) is not int:
            errors['next_stop'] += 1
        if item['stop_type'] not in STOP_TYPE and item['stop_type'] != '':
            errors['stop_type'] += 1
        if not check_name(item['stop_name']):
            errors['stop_name'] += 1
        if not check_time(item['a_time']):
            errors['a_time'] += 1
    print(f'Type and required field validation: {sum(c for c in errors.values())} errors')
    for error, count in errors.items():
        if error in ['stop_type', 'stop_name', 'a_time']:
            print(f'{error}: {count}')


def get_bus_line_info(json_obj):
    info = {}
    for item in json_obj:
        if item['bus_id'] in info:
            info[item['bus_id']] += 1
        else:
            info[item['bus_id']] = 1

    for bus_id, stops in info.items():
        print(f'bus_id: {bus_id}, stops: {stops}')


def check_start_stop(json_obj):
    start_final = {}
    for item in json_obj:
        if item['stop_type'] in ['S', 'F']:
            if start_final.get(item['bus_id']):
                start_final[item['bus_id']].append(item['stop_type'])
            else:
                start_final[item['bus_id']] = []
                start_final[item['bus_id']].append(item['stop_type'])
    for key, value in start_final.items():
        if len(value) != 2:
            return key
    return -1


def get_stop_type_info(json_obj):
    start_stops = list(set(item["stop_name"] for item in list(filter(lambda item: item['stop_type'] == 'S', json_obj))))
    finish_stops = list(set(item["stop_name"] for item in list(filter(lambda item: item['stop_type'] == 'F', json_obj))))
    list.sort(start_stops)
    list.sort(finish_stops)
    buses_stops = {}
    for item in json_obj:
        if item['stop_name'] in buses_stops:
            buses_stops[item['stop_name']].add(item['bus_id'])
        else:
            buses_stops[item['stop_name']] = set()
            buses_stops[item['stop_name']].add(item['bus_id'])

    transfer_stops = list(set(key for key, value in buses_stops.items() if len(value) >= 2))
    list.sort(transfer_stops)
    print(f'Start stops: {len(start_stops)} {start_stops}')
    print(f'Transfer stops: {len(transfer_stops)} {transfer_stops}')
    print(f'Finish stops: {len(finish_stops)} {finish_stops}')


def main():
    json_obj = json.loads(json_str)
    incorrect_bus = check_start_stop(json_obj)
    if incorrect_bus == -1:
        get_stop_type_info(json_obj)
    else:
        print(f'There is no start or end stop for the line: {incorrect_bus}.')
    # check_json_data(json_obj)
    # print(json.dumps(json_obj, indent=4))


if __name__ == '__main__':
    main()
