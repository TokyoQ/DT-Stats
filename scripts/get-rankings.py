import requests
import json
import csv
import os
import numpy as np
from datetime import datetime
from lib2to3.fixer_util import String

def esc(text):
    return text.encode('utf-8')
    #text.replace("'", "''").replace(u"\u2018", "'").replace(u"\u2019", "'")

# INIT
CURRENT_ROUND = 5

url_base = "https://fantasy.afl.com.au/afl_classic/api"
path = "teams_classic/rankings"

url = "{}/{}".format(url_base, path)

offset = 0
team_ranks = []

# Prepare output file
outputPath = "/Users/aleccollier/Documents/workspace/fantasy-scrape/DT-Stats/output"
outputFilename = "rankings-rd{}.csv".format(CURRENT_ROUND)
outputFile = '{}/{}'.format(outputPath, outputFilename)
header = ["round","user_id","team_id","first_name","last_name","team_name","round_points","round_rank","overall_points","overall_rank","value"]

with open(outputFile, "w") as output:
    writer = csv.writer(output)
    writer.writerow(header)

# Loop through rankings
while offset % 50 == 0:
    # Make the request
    parameters = {"offset": offset, "order_direction": "ASC", "order": "rank"}
    raw = requests.get(url, params = parameters)
    response = json.loads(raw.text)

    if len(response["errors"]) > 0:
        print("Error encountered!")
        exit(1)

    with open(outputFile, "a") as output:
        ranks = response["result"]
        writer = csv.writer(output)

        for rank in ranks:
            round = CURRENT_ROUND
            user_id = rank["user_id"]
            team_id = rank["team_id"]
            first_name = rank["firstname"]
            last_name = rank["lastname"]
            team_name = rank["team_name"]
            round_points = rank["this_round_points"]
            round_rank = rank["rank_history"][str(CURRENT_ROUND)]
            overall_points = rank["league_points"]
            overall_rank = rank["overall_rank"]
            value = rank["value"]

            line = [round, user_id, team_id, esc(first_name), esc(last_name), esc(team_name), round_points, round_rank, overall_points, overall_rank, value]
            writer.writerow(line)

            '''
            team_rank = {}
            team_rank["round"] = CURRENT_ROUND
            team_rank["user_id"] = rank["user_id"]
            team_rank["team_id"] = rank["team_id"]
            team_rank["first_name"] = rank["firstname"]
            team_rank["last_name"] = rank["lastname"]
            team_rank["team_name"] = rank["team_name"]
            team_rank["round_points"] = rank["this_round_points"]
            team_rank["round_rank"] = rank["rank_history"][str(CURRENT_ROUND)]
            team_rank["overall_points"] = rank["league_points"]
            team_rank["overall_rank"] = rank["overall_rank"]
            team_rank["value"] = rank["value"]
    
            team_ranks.append(team_rank)
            '''

            offset = overall_rank
