'''uname =""
fname =""
lname =""
country =""'''
import sqlite3


con = sqlite3.connect("database.db")
c = con.cursor()
result = c.execute("SELECT * FROM userdata")
result = result.fetchall()
i = 0
while (result.__len__() > i):
    # for a in result:
    #    asd.update(a[0],a[2],a[3],a[4])

    print(result[i])
    i= i+1
