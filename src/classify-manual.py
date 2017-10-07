#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import pyperclip

MANUAL_PATH = sys.argv[1]

for filename in os.listdir(MANUAL_PATH):
    print(chr(27) + "[2J")
    if(filename in ['pos', 'neg', 'neu']):
        continue
    file = open("%s%s" % (MANUAL_PATH, filename), 'r')
    file_content = file.read()
    print filename
    print file_content
    choice = raw_input("opção: ")
    while(choice not in (['pos', 'neg', 'neu', 'exit', 'cp'])):
        print 'Comendo não encontrado. '
        choice = raw_input("opção: ")
    if (choice == 'cp'):
        pyperclip.copy(file_content)
        print "Copiado para área de transferência!"
        choice = raw_input("Classificação: ")
        while (choice not in (['pos', 'neg', 'neu', 'exit'])):
            print 'Comendo não encontrado.'
            choice = raw_input("Classificação: ")
    if (choice == 'exit'):
        break
    os.rename("%s%s" % (MANUAL_PATH, filename), "%s%s/%s" % (MANUAL_PATH, choice, filename))
