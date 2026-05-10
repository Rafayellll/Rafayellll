import sqlite3

conn = sqlite3.connect('portal.db')
with open('schema.sql', 'w') as f:
    for line in conn.iterdump():
        f.write(line + '\n')
conn.close()
