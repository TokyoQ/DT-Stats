import requests
import json
import mysql.connector

def esc(text):
    return text.replace("'","''")

url="https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/players.json"

raw = requests.get(url)
players = json.loads(raw.text)

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

for player in players:
    id = player['id']
    year = "2017"
    first = esc(player['first_name'])
    last = esc(player['last_name'])
    squad = player['squad_id']
    posns = [0,0,0,0]
    
    for pos in player['positions']:
        if pos == 1:
            posns[0] = 1
        if pos == 2:
            posns[1] = 1
        if pos == 3:
            posns[2] = 1
        if pos == 4:
            posns[3] = 1
    
    query = """REPLACE INTO players 
    (id,year,firstname,lastname,squad_id,def,mid,ruc,fwd) 
    VALUES 
    ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}')""".format(id,year,first,last,squad,posns[0],posns[1],posns[2],posns[3])
    
    #print query
    cursor.execute(query)
    dbconn.commit() 
    
cursor.close()
dbconn.close()
    