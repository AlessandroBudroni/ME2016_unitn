import sqlite3
import extract_keywords_from_text as ke

db_file = 'dev.db'
conn = sqlite3.connect(db_file)
c = conn.cursor()

res = c.execute('SELECT * FROM website_from_img')

for row in res:
    mostFreqWords = ke.tag(row[2])
    print(mostFreqWords)
