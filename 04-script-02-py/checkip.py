#!/usr/bin/env python3

import os
import socket
import pickle
import json
import yaml


def checkip(hostname):
    a_dict = {}
    dictionarypath = "/home/vagrant/dns/saved_dictionary.pkl"
    jsonpath = "/home/vagrant/dns/saved_dictionary.json"
    yamlpath = "/home/vagrant/dns/saved_dictionary.yaml"

    fileexist = os.access(dictionarypath, os.F_OK)
    jsonexist = os.access(jsonpath, os.F_OK)
    yamlexist = os.access(yamlpath, os.F_OK)

    if fileexist:
        with open(dictionarypath, 'rb') as f:
            a_dict = pickle.load(f)
    else:
        os.popen('touch "/home/vagrant/dns/saved_dictionary.pkl"')
    
    if jsonexist is False:
        os.popen('touch "/home/vagrant/dns/saved_dictionary.json"')

    if yamlexist is False:
        os.popen('touch "/home/vagrant/dns/saved_dictionary.yaml"')

    ip = socket.gethostbyname(hostname)

    try:
        check = a_dict[hostname]
    except KeyError:
        a_dict.update({hostname:ip})
        check = a_dict[hostname]

    if check != ip:
        print("[ERROR] " + hostname + " IP mismatch: " + a_dict[hostname] + " " + ip)
        a_dict.update({hostname:ip})

        with open(dictionarypath, 'wb') as f:
            pickle.dump(a_dict, f)
        with open(jsonpath, 'w') as f:
            json.dump(a_dict, f)
        with open(yamlpath, 'w') as f:
            yaml.dump(a_dict, f)

        print("в словарь был записан новый ip " + hostname + ' - ' + ip)
    else:
        with open(dictionarypath, 'wb') as f:
            pickle.dump(a_dict, f)
        with open(jsonpath, 'w') as f:
            json.dump(a_dict, f)
        with open(yamlpath, 'w') as f:
            yaml.dump(a_dict, f)

        print(hostname + ' - ' + ip)

checkip("google.com")
checkip("yandex.ru")
checkip("netology.ru")