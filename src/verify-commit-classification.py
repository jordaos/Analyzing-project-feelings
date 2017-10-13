import sys
import os
import os.path

# HOW TO USE THIS:
# python src/verify-commit-classification.py BRANCH SHA METHOD
# BRANCH: eg.: branch-0.2
# SHA: eg.: 3456uiksdnbvsfaydsaudyusyduaadu7
# METHOD: {manual, naivebayes, sentistrength}
# this produces a classification of the commit ("pos", "neg", "neu" or "none")

BRANCH = ''
SHA = ''
METHOD = ''

if len(sys.argv) > 3:
    BRANCH = sys.argv[1]
    SHA = sys.argv[2]
    METHOD = sys.argv[3]
else:
    print 'Give all parameters'
    sys.exit()

OS_PATH = '/home/jordao/MEGAsync/projeto_bolsa/Analyzing-project-feelings/data/hadoop_messages/' + BRANCH
CLASSIFICATION_PATH = OS_PATH + '/' + METHOD

def has_in():
    thisIs = 'none'
    classifications = ['pos', 'neu', 'neg']
    for classification in classifications:
        file_path = CLASSIFICATION_PATH + '/' + classification+ '/' + SHA + '.txt'
        if os.path.exists(file_path):
            thisIs = classification
            break
    print(thisIs)

has_in()