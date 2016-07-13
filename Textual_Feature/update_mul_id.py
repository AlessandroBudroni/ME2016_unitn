import sqlite3

db2 = 'text_from_media.db'
db2_path = '../Text_Retrieval/dataset/testset/' + db2
# connect to database
conn = sqlite3.connect(db2_path)
c = conn.cursor()

c.execute('SELECT mul_id from website_from_img')
all_mul_id = c.fetchall()
for m in all_mul_id:
    m_ = m[0].strip('\n\t ')
    c.execute('UPDATE website_from_img SET mul_id=? WHERE mul_id=?', (m_,m[0]))
    conn.commit()

conn.close()