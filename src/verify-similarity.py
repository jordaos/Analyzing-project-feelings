#coding: utf-8

from os import listdir
from os.path import isfile, join
import sys
from time import gmtime, strftime

MANUAL_CLASSIFICATION = sys.argv[1]
MODEL_CLASSIFICATION = sys.argv[2]
FILE_NAME = sys.argv[3]

def is_in(dir, file, cat):
    dir_cat = dir + cat + "/"
    for f in listdir(dir_cat):
        if isfile(join(dir_cat, f)):
            if(f == file):
                return True
    return False


def verify_is(log_file, dir, cat, dir2, link):
    texto = ""
    dir_cat = dir + cat + "/"
    for f in listdir(dir_cat):
        if isfile(join(dir_cat, f)):
            if(is_in(dir2, f, cat) != True):
                categories = ["pos", "neg", "neu"]
                categories.remove(cat)
                for categ in categories:
                    if (is_in(dir2, f, categ) == True):
                        texto += "- <a href=\"%s/%s/%s\">%s</a> deveria ser \"%s\", mas está em \"%s\" \n" % (link, categ, f, f, categ, cat)
            else:
                texto += "- <a href=\"%s/%s/%s\">%s</a> está certo (%s)\n" % (link, cat, f, f, cat)
    log_file.write(texto)



# dir_ver1 = '../raw-data/1_release_hadoop_classified_sentistrength1/'
# dir_ver2 = '../raw-data/1_release_hadoop_classified_manual/'

def verify():
    log = open('%s' % (FILE_NAME), 'a')
    texto = "# %s \n" % (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    log.write(texto)
    link = "https://github.com/jordaos/Analyzing-Hadoop-feelings/tree/master/raw-data/%s" % \
           ((MANUAL_CLASSIFICATION.split("/"))[-2])

    verify_is(log, MODEL_CLASSIFICATION, "pos", MANUAL_CLASSIFICATION, link)  # Verificar os positivos
    verify_is(log, MODEL_CLASSIFICATION, "neg", MANUAL_CLASSIFICATION, link)  # Verificar os negativos
    verify_is(log, MODEL_CLASSIFICATION, "neu", MANUAL_CLASSIFICATION, link)  # Verificar os neutros

    log.close()

verify()