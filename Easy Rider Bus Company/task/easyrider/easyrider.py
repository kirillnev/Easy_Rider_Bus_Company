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


def check_name(name):
    re_tmpl = rf'^[A-Z][\w ]+({"|".join(STOP_NAME_SUFFIX)})$'
    return re.match(re_tmpl, str(name)) is not None


def check_time(time):
    re_tmpl = r'^(0\d|1\d|2[0-3]):[0-5]\d$'
    return re.match(re_tmpl, str(time)) is not None


def main():
    json_obj = json.loads(json_str)
    # print(json.dumps(json_obj, indent=4))

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


if __name__ == '__main__':
    main()
