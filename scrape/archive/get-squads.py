import requests
import json
import mysql.connector

def esc(text):
    return text.replace("'","''")

url="https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/squads.json"

raw = requests.get(url)
squads = json.loads(raw.text)

#Connect to db
try:
    dbconn = mysql.connector.connect(user='root',password='test1',host='127.0.0.1',database='fantasy')
    cursor = dbconn.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print "Unknown error."
    print(err)

for squad in squads:
    id = squad['id']
    full = esc(squad['full_name'])
    name = esc(squad['name'])
    short = esc(squad['short_name'])
    
    query = "REPLACE INTO squads (id,fullname,name,shortname) VALUES ('{0}','{1}','{2}','{3}')".format(id,full,name,short)
    cursor.execute(query)
    dbconn.commit() 
    
cursor.close()
dbconn.close()
    