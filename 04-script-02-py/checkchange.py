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