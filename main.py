import json
import os

file_path = "/data/apps/serveStatus/config.json"


def read_config():
    with open(file=file_path, mode='r', encoding="utf-8") as config_stream:
        config_json = json.load(config_stream)
    return config_json


def write_config(config_json: dict):
    with open(file=file_path, mode='w', encoding="utf-8") as config_stream:
        json.dump(config_json, config_stream, indent=4, ensure_ascii=False)


def restart_server():
    os.system("systemctl restart serveStatus")


def add_server():
    print('====== Add Server ======')
    username = input('Please input username: ')
    name = input('Please input name: ')
    type = input('Please input type: ')
    host = input('Please input host: ')
    location = input('Please input location: ')
    password = input('Please input password: ')
    monthstart = int(input('Please input monthstart: '))
    print(
        f'====== INFO ======\n'
        f'username : {username} \n'
        f'name : {name} \n'
        f'type : {type} \n'
        f'host : {host} \n'
        f'location : {location} \n'
        f'password : {password} \n'
        f'monthstart : {monthstart} \n'
        f'====== END ======\n'

    )
    is_enter = input('Press ENTER continue')
    if is_enter != '':
        print("ERROR INPUT: RETURN")
        return
    print("Start Adding......")
    config_json = read_config()

    for item in config_json['servers']:
        check_username = item["username"]
        if check_username == username:
            print('ERROR: Username has been used!!!')
            return

    server_dict = {
        "username": username,
        "name": name,
        "type": type,
        "host": host,
        "location": location,
        "password": password,
        "monthstart": monthstart
    }
    config_json['servers'].append(server_dict)
    write_config(config_json)
    restart_server()
    print("ADD SUCCESSFULLY")


def del_server():
    print("====== Select Username To Delete")
    config_json = read_config()
    for item in config_json["servers"]:
        print("- Username: " + item["username"])
    username = input("Please input username: ")
    if not username or not len(username.strip()):
        print("ERROR: No Input")
        return

    for item in config_json["servers"]:
        if item["username"] == username:
            config_json["servers"].remove(item)

    write_config(config_json)
    restart_server()
    print("DELETE SUCCESSFULLY")


def exit_script():
    exit(0)


def task_select(select_num):
    numbers = {
        1: add_server,
        2: del_server,
        3: exit_script
    }
    method = numbers.get(select_num)
    if method:
        method()


def start():
    while True:
        print(
            '====== Welcome to use ServerStatus manage script:\n'
            '- 1. Add Server \n'
            '- 2. Del Server \n'
            '- 3. Exit \n'
            '====== END ======'
        )
        select_num = input("Please input the select num: ")

        task_select(int(select_num))


if __name__ == '__main__':
    start()
