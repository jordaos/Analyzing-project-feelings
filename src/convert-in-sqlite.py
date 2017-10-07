import sqlite3
import re
import sys

BRANCH = ''

if len(sys.argv) > 1:
    BRANCH = sys.argv[1]
else:
    print('Give parameter')
    sys.exit()

# File containing SentiStrength analysis
# 0: POS | 1: NEG | 2: TEXT | 3: Explanation
ss_analysis = 'data/hadoop_messages/' + BRANCH + '/' + BRANCH + '-filtered0_out.txt'
arq = open(ss_analysis, 'r')
commit_analysis = arq.readline()

conn = sqlite3.connect('data/hadoop_messages/' + BRANCH + '/' + BRANCH + '.sqlite')
# 0: Project | 1: sha | 2: message | 3: date | 4: author_name | 5: author_email
cursor = conn.cursor()

# database sentiments configuration
# new_db_conn = sqlite3.connect('../data/2_release_analysis_ss_filter.sqlite')
# nwc = new_db_conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS `sentiment` 
                ( `project` TEXT, 
                `sha` TEXT, 
                `Positive` INTEGER, 
                `Negative` INTEGER, 
                `Text` TEXT, 
                `Explanation` TEXT )''')

# lendo os dados
cursor.execute("""
SELECT * FROM commits;
""")

for linha in cursor.fetchall():
    commit_analysis = arq.readline()
    arr_analysis = re.split(r'\t+', commit_analysis)
    cursor.execute("""
    INSERT INTO sentiment (project, sha, Positive, Negative, Text, Explanation)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (linha[0], linha[1], arr_analysis[0], arr_analysis[1], linha[2], arr_analysis[3]))

conn.commit()
conn.close()