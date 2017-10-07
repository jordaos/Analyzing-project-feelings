import sqlite3
import sys

BRANCH = ''

if len(sys.argv) > 1:
    BRANCH = sys.argv[1]
else:
    print 'Give parameter'
    sys.exit()

PATH = 'data/hadoop_messages/' + BRANCH
DB = PATH + '/' + BRANCH + '.sqlite'

conn = sqlite3.connect(DB)
cursor = conn.cursor()
# lendo os dados
cursor.execute("""
SELECT * FROM commits;
""")

# Change it!
folder_name = "3_release_hadoop"

for linha in cursor.fetchall():
    file = open("%s/all/%s.txt" % (PATH, linha[1]), "w")
    file.write(linha[2])
    file.close()
conn.close()