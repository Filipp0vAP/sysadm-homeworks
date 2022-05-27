# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательные задания

1. Есть скрипт:
	```python
    #!/usr/bin/env python3
	a = 1
	b = '2'
	c = a + b
	```
	* Какое значение будет присвоено переменной c?
	* Как получить для переменной c значение 12?
	* Как получить для переменной c значение 3?
	
	
	## Ответ
	
	* Какое значение будет присвоено переменной c?
	а никакое, выдаст ошибку потому что нельзя складывать строку с числом
	
	* Как получить для переменной c значение 12?
	конвертировать переменную a в строку - str(a), то есть строка присвоения значения переменной с будет выглядеть вот так c = str(a) + b
	
	* Как получить для переменной c значение 3?
	конвертировать b в  число - c = a + int(b)
	
	---
	
1. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

	```python
    #!/usr/bin/env python3

    import os

	bash_command = ["cd ~/netology/sysadm-homeworks/", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False
	for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = result.replace('\tmodified:   ', '')
            print(prepare_result)
            break

	```

	## Ответ
	
	```python
	#!/usr/bin/env python3

	import os
	
	
	gitpath = "~/netology/netology-sysadm-homeworks/"
	bash_command = ["cd " + gitpath, "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()

	for result in result_os.split('\n'):
	    if result.find('modified') != -1:
		prepare_result = result.replace('\tmodified:   ', '')
		print(gitpath + prepare_result)
	
	```
	убрал лишний break и лишнюю перменную is_change.
	А так же завернул путь до репы в переменную и потом ее склеиваю с результатом вывода. Так понятнее где нужные файлы
	---
	
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

	## Ответ

	```python
	#!/usr/bin/env python3

	import os
	import sys


	def GetModified(gitpath):
	    bash_command2 = ["cd " + gitpath, "git status"]
	    result_os = os.popen(' && '.join(bash_command2)).read()

	    for result in result_os.split('\n'):
		if result.find('modified') != -1:
		    prepare_result = result.replace('\tmodified:   ', '')
		    print(gitpath + prepare_result)

	def ChechGitFolder(checkpath):
	    bash_command = ["cd " + checkpath, "pwd"]
	    fullpath = os.popen(' && '.join(bash_command)).read()
	    fullpath = fullpath.replace('\n','')
	    check = os.path.isdir(fullpath + "/.git")

	    if check is False:
		print("похоже вы указали директорию где нет git репозитория")
		sys.exit()


	userpath = sys.argv[1]
	ChechGitFolder(userpath)
	GetModified(userpath)
	```
	
	---
	
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.
	
	## Ответ
	
	```python
	#!/usr/bin/env python3

	import os
	import socket
	import pickle


	def checkip(hostname):
	    a_dict = {}
	    dictionarypath = "/home/vagrant/dns/saved_dictionary.pkl"
	    fileexist = os.access(dictionarypath, os.F_OK)

	    if fileexist:
		with open(dictionarypath, 'rb') as f:
		    a_dict = pickle.load(f)
	    else:
		os.popen('touch "/home/vagrant/dns/saved_dictionary.pkl"')

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
		print("в словарь был записан новый ip " + hostname + ' - ' + ip)
	    else:
		with open(dictionarypath, 'wb') as f:
		    pickle.dump(a_dict, f)
		print(hostname + ' - ' + ip)

	checkip("google.com")
	checkip("yandex.ru")
	checkip("netology.ru")
	
	```
	
	пример вывода:
	
	```bash
	google.com - 216.58.210.174
	[ERROR] yandex.ru IP mismatch: 77.88.55.66 5.255.255.55
	в словарь был записан новый ip yandex.ru - 5.255.255.55
	netology.ru - 188.114.99.171
	
	```
	
	
	---
## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 


---

### Как сдавать задания

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
