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


def check_arrival_time(json_obj):
    bus_ids = set(item["bus_id"] for item in json_obj)
    print('Arrival time test:')
    is_ok = True
    for bus_id in bus_ids:
        cur_stops = {item['stop_id']: item for item in json_obj if item['bus_id'] == bus_id}
        start_stop_id = -1
        for stop_id, value in cur_stops.items():
            if value['stop_type'] == 'S':
                start_stop_id = stop_id
                break
        cur_id = start_stop_id
        while True and cur_stops[cur_id]['next_stop'] != 0:
            # print(cur_stops[cur_id])
            # print(cur_stops[cur_stops[cur_id]['next_stop']])
            # print(cur_stops[cur_id]['a_time'] >= cur_stops[cur_stops[cur_id]['next_stop']]['a_time'])
            if cur_stops[cur_id]['a_time'] >= cur_stops[cur_stops[cur_id]['next_stop']]['a_time']:
                break
            cur_id = cur_stops[cur_id]['next_stop']
        if cur_stops[cur_id]['next_stop'] != 0:
            is_ok = False
            print(f'bus_id line {cur_stops[cur_id]["bus_id"]}: wrong time on station {cur_stops[cur_stops[cur_id]["next_stop"]]["stop_name"]}')
    if is_ok:
        print('OK')


def check_buses_type(json_obj):
    print('On demand stops test:')
    stops_set = set(item['stop_id'] for item in json_obj)
    invalid_stops = set()
    for stop in stops_set:
        cur_stops = [item for item in json_obj if item['stop_id'] == stop]
        for item in cur_stops:
            if len(cur_stops) > 1 and item['stop_type'] == 'O':
                invalid_stops.add(item['stop_name'])
    print(f'Wrong stop type: {list(invalid_stops)}' if len(invalid_stops) > 0 else 'OK')

def main():
    json_obj = json.loads(json_str)
    check_buses_type(json_obj)
    # check_arrival_time(json_obj)
    # incorrect_bus = check_start_stop(json_obj)
    # if incorrect_bus == -1:
    #     get_stop_type_info(json_obj)
    # else:
    #     print(f'There is no start or end stop for the line: {incorrect_bus}.')
    # check_json_data(json_obj)
    # print(json.dumps(json_obj, indent=4))


if __name__ == '__main__':
    main()
