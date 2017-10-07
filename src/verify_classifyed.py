import sys
import os
import os.path

CLASSIFIED = sys.argv[1]
TO_VERIFY = sys.argv[2]

def has_in(filename):
    classifications = ['pos', 'neu', 'neg']
    for classification in classifications:
        file_path = "%s/%s/%s" % (CLASSIFIED, classification, filename)
        if os.path.exists(file_path):
            os.rename("%s/%s" % (TO_VERIFY, filename), "%s/%s/%s" % (TO_VERIFY, classification, filename))
            break

for filename in os.listdir(TO_VERIFY):
    has_in(filename)