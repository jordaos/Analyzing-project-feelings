import math
import sqlite3
import sys

BRANCH = ''

if len(sys.argv) > 1:
    BRANCH = sys.argv[1]
else:
    print('Give parameter')
    sys.exit()

# Change it!
dir = 'data/hadoop_messages/' + BRANCH + '/sentistrength'
conn = sqlite3.connect('data/hadoop_messages/' + BRANCH + '/' + BRANCH + '.sqlite')
# 0: project | 1: sha | 2: positive | 3: negative | 4: text | 5: Explanation
cursor = conn.cursor()
# lendo os dados
cursor.execute("""
SELECT * FROM sentiment;
""")

for linha in cursor.fetchall():
    message = linha[4]
    sha = linha[1]
    pos = math.fabs(linha[2])
    neg = math.fabs(linha[3])
    # print (message + ' | ' + sha + ' | ' + pos + ' ' + neg)

    if pos == neg:
        with open("%s/neu/%s.txt" % (dir, sha), "a") as arq:
            arq.write(message)
            arq.close()
    elif pos > neg:
        with open("%s/pos/%s.txt" % (dir, sha), "a") as arq:
            arq.write(message)
            arq.close()
    else:
        with open("%s/neg/%s.txt" % (dir, sha), "a") as arq:
            arq.write(message)
            arq.close()

