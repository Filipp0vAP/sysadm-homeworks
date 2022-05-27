# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
	```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
	```
	Нужно найти и исправить все ошибки, которые допускает наш сервис
	
	## Ответ
	
	не хватало ковычек в строке "ip" : "71.78.22.43"
	добавил в Json выше
	
	---
	
  
2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.
	
	## Ответ
	
	```python
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
	
	```
	
	---
## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

---

### Как сдавать задания

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
