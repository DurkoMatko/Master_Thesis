#Server Connection to MySQL:
import MySQLdb

conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="root",
                  db="oss_issues")
handle = conn.cursor()

try:
   handle.execute("""INSERT INTO oss_issues.issues (title,number,created,closed,description,labels,project) VALUES (%s,%s,CURDATE(),CURDATE(),%s,%s,%s)""",('testTitle','0','testDescription','testLabel','testProj'))
   conn.commit()
   print 'done'
except Exception as e:
   conn.rollback()
   print(e)

conn.close()