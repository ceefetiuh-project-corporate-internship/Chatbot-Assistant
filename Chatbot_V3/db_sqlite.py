##tao khohang.db
import sqlite3

conn = sqlite3.connect('khohangrasa.db')

print ("Opened database successfully")

#conn.execute('''CREATE TABLE KHOHANG(
#        linh_kien      TEXT PRIMARY KEY NOT NULL,
#	     loai_linh_kien	TEXT NOT NULL,
#	     gia            INTEGER NOT NULL);''')
#print ("Table created successfully")

#conn.execute("INSERT INTO KHOHANG (linh_kien, loai_linh_kien, gia) \
#      VALUES ('c1815', 'transistor', 100 )")

#conn.execute("INSERT INTO KHOHANG (linh_kien, loai_linh_kien, gia) \
#      VALUES ('bc337', 'transistor', 150 )")

#conn.execute("INSERT INTO KHOHANG (linh_kien, loai_linh_kien, gia) \
#      VALUES ('2n3904', 'transistor', 200 )")

#conn.commit()
#print ("Records created successfully")

cursor = conn.execute("SELECT linh_kien, loai_linh_kien, gia from KHOHANG")
for row in cursor:
   print ("linh_kien = ", row[0])
   print ("loai_linh_kien = ", row[1])
   print ("gia = ", row[2], "\n")

print ("Operation done successfully")

conn.close()