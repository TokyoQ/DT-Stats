import requests
import json
import mysql.connector

def esc(text):
    return text.replace("'","''")

url="https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/venues.json"

raw = requests.get(url)
venues = json.loads(raw.text)

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

#add_venue = ("INSERT INTO venues (id,name,short_name,timezone) VALUES (%(id)s,%(name)s,%

for venue in venues:
    #print "id="+venue['id']+", name="+venue['name']+", short="+venue["short_name"]+", timezone="+venue['timezone']
    id = venue['id']
    name = esc(venue['name'])
    short = esc(venue['short_name'])
    timezone = esc(venue['timezone'])
    
    query = "REPLACE INTO venues (id,name,short_name,timezone) VALUES ('{0}','{1}','{2}','{3}')".format(id,name,short,timezone)
    cursor.execute(query)
    dbconn.commit() 
    
cursor.close()
dbconn.close()
    