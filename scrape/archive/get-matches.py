import requests
import json
import mysql.connector
from datetime import datetime
from lib2to3.fixer_util import String

def esc(text):
    return text.replace("'","''")

url="https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/rounds.json"

CURRENT_ROUND=18
raw = requests.get(url)
rounds = json.loads(raw.text)

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

for round in rounds:
    
    matches = round['matches']
    
    for match in matches:
        id = match['id']
        year = '2017'
        round = match['round']
        #date = datetime.strptime(match['date'],'%Y-%m-%d %H:%M:%S')
        date = match['date']
        venue_id = match['venue_id']
        home_id = match['home_squad_id']
        away_id = match['away_squad_id']
        partial = int(match['lockout'] == 'partial') 
        home_score = match['home_score']
        away_score = match['away_score']
        
        if round > CURRENT_ROUND:
            continue
        
        query = """ REPLACE INTO matches 
        (id,year,round,date,venue_id,home_id,away_id,partial_lockout,home_score,away_score) 
        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')
        """.format(id,year,round,date,venue_id,home_id,away_id,partial,home_score,away_score)
        cursor.execute(query)

    dbconn.commit()

cursor.close()
dbconn.close()
    