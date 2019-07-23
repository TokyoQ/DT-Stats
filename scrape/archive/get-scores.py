import requests
import json
import mysql.connector
from datetime import datetime
from lib2to3.fixer_util import String

def esc(text):
    return text.replace("'","''")

CURRENT_ROUND=18

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


#ROUNDS
url_base="https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/stats/"

for round in range(1,CURRENT_ROUND):
    url=url_base+str(round)+".json"
    raw = requests.get(url)
     
    players = json.loads(raw.text)
 
    for player in players:
        year = '2017'
        player_id = player
        kicks = players[player]['K']
        handballs = players[player]['H']
        marks = players[player]['M']
        tackles = players[player]['T']
        frees_for = players[player]['FF']
        frees_against = players[player]['FA']
        hitouts = players[player]['H']
        goals = players[player]['G']
        behinds = players[player]['B']
        tog = players[player]['TOG']
         
        score = 3*kicks+2*handballs+3*marks+4*tackles+1*frees_for-3*frees_against+1*hitouts+6*goals+1*behinds
         
        query = """ REPLACE INTO scores 
        (year,round,player_id,kicks,handballs,marks,tackles,hitouts,frees_for,frees_against,goals,behinds,tog,score) 
        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}',{10},{11},{12},{13})
        """.format(year,round,player_id,kicks,handballs,marks,tackles,hitouts,frees_for,frees_against,goals,behinds,tog,score)
        cursor.execute(query)
     
    dbconn.commit()

#PLAYERS
url = "https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/players.json"
raw = requests.get(url)

players = json.loads(raw.text)

for player in players:
    year = 2017
    player_id = player['id']
    squad_id = player['squad_id']
    
    stats = player['stats']
    for round in stats['prices']:
        
        if int(round) > CURRENT_ROUND:
            continue
        
        price = stats['prices'][round]
        
        #print "UPDATE scores SET price = {3} AND squad_id = {4} WHERE year = {0} AND round = {1} AND player_id = {2}".format(year,round,player_id,price,squad_id)
        query = "UPDATE scores SET price = {3}, squad_id = {4} WHERE year = {0} AND round = {1} AND player_id = {2}".format(year,round,player_id,price,squad_id)
        cursor.execute(query)

    dbconn.commit()

#MATCHES
url = "https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/rounds.json"
raw = requests.get(url)

rounds = json.loads(raw.text)
year = 2017 

for round in rounds:
    
    for match in round['matches']:
        roundNum = match['round']
        home_id = match['home_squad_id']
        away_id = match['away_squad_id']
        venue_id = match['venue_id']
     
        if int(roundNum) > CURRENT_ROUND:
            continue
         
        #print "UPDATE scores SET squad_against_id = {3}, venue_id = {4} WHERE year = {0} AND round = {1} AND squad_id = {2}".format(year,roundNum,home_id,away_id,venue_id)
        query = "UPDATE scores SET squad_against_id = {3}, venue_id = {4} WHERE year = {0} AND round = {1} AND squad_id = {2}".format(year,roundNum,home_id,away_id,venue_id)
        cursor.execute(query)
        
        #print "UPDATE scores SET squad_against_id = {3}, venue_id = {4} WHERE year = {0} AND round = {1} AND squad_id = {2}".format(year,roundNum,away_id,home_id,venue_id)
        query = "UPDATE scores SET squad_against_id = {3}, venue_id = {4} WHERE year = {0} AND round = {1} AND squad_id = {2}".format(year,roundNum,away_id,home_id,venue_id)
        cursor.execute(query)
 
    dbconn.commit()

cursor.close()
dbconn.close()
    