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
CURRENT_ROUND = 2

url_base = "https://fantasy.afl.com.au/afl_classic/api"
path = "teams_classic/show"

url = "{}/{}".format(url_base, path)

teams = []

# Prepare output file
outputPath = "/Users/aleccollier/Documents/workspace/fantasy-scrape/DT-Stats/output"
outputFilename = "teams-rd2.csv"
outputFile = '{}/{}'.format(outputPath, outputFilename)

rankingsFilename = "rankings-rd2.csv"
rankingsFile = '{}/{}'.format(outputPath, rankingsFilename)

header = ["round","team_id","user_id","team_name","overall_points","def_1","def_2","def_3","def_4","def_5","def_6","mid_1","mid_2","mid_3","mid_4","mid_5","mid_6","mid_7","mid_8","ruc_1","ruc_2","fwd_1","fwd_2","fwd_3","fwd_4","fwd_5","fwd_6","def_7","def_8","mid_9","mid_10","ruc_3","ruc_4","fwd_7","fwd_8","captain","vice_captain","emergency_1","emergency_2","emergency_3","emergency_4"]

with open(outputFile, "w") as output:
    writer = csv.writer(output)
    writer.writerow(header)

# Loop through rankings
done = False
while not done:

    # Get id's from other csv
    team_ids = []
    with open(rankingsFile, "r") as rankings:
        reader = csv.reader(rankings)
        next(reader)
        for row in reader:
            team_id = row[2]
            team_ids.append(team_id)

    # Get team by id
    for team_id in team_ids:
        parameters = {"id": team_id}

        headers = {
            "cookie": "AWSALB=bAhPPv1xEGZ1tz0+/RB6CLS1/huDAUzUQHlktsDCNdIgwfLMrgP8wPNUlRY7iu7M0UWqj9/bfZLFeKaPGR3elWIOY2kb4ahn3sYduu2u0dh5e9RLa4CC20E5ArM6",
            "cookie": "session=6ed13a8ed4ac25cc18c435442071d71644681e82"
        }
        raw = requests.get(url, params=parameters, headers=headers)

        response = json.loads(raw.text)
        errors = response["errors"]

        if len(errors) > 0:
            print("Error encountered for team id {}".format(team_id))
            print(errors)
            exit(1)

        team = response["result"]

        round = CURRENT_ROUND
        team_id = team["id"]
        user_id = team["user_id"]
        team_name = esc(team["name"])
        overall_points = team["points"]

        try:
            def_1 = team["lineup"]["1"][0]
            def_2 = team["lineup"]["1"][1]
            def_3 = team["lineup"]["1"][2]
            def_4 = team["lineup"]["1"][3]
            def_5 = team["lineup"]["1"][4]
            def_6 = team["lineup"]["1"][5]

            mid_1 = team["lineup"]["2"][0]
            mid_2 = team["lineup"]["2"][1]
            mid_3 = team["lineup"]["2"][2]
            mid_4 = team["lineup"]["2"][3]
            mid_5 = team["lineup"]["2"][4]
            mid_6 = team["lineup"]["2"][5]
            mid_7 = team["lineup"]["2"][6]
            mid_8 = team["lineup"]["2"][7]

            ruc_1 = team["lineup"]["3"][0]
            ruc_2 = team["lineup"]["3"][1]

            fwd_1 = team["lineup"]["4"][0]
            fwd_2 = team["lineup"]["4"][1]
            fwd_3 = team["lineup"]["4"][2]
            fwd_4 = team["lineup"]["4"][3]
            fwd_5 = team["lineup"]["4"][4]
            fwd_6 = team["lineup"]["4"][5]

            def_7 = team["lineup"]["bench"]["1"][0]
            def_8 = team["lineup"]["bench"]["1"][1]
            ruc_3 = team["lineup"]["bench"]["2"][0]
            ruc_4 = team["lineup"]["bench"]["2"][1]
            mid_9 = team["lineup"]["bench"]["3"][0]
            mid_10 = team["lineup"]["bench"]["3"][1]
            fwd_7 = team["lineup"]["bench"]["4"][0]
            fwd_8 = team["lineup"]["bench"]["4"][1]

            emergency_1 = team["lineup"]["bench"]["emergency"][0]
            emergency_2 = team["lineup"]["bench"]["emergency"][1]
            emergency_3 = team["lineup"]["bench"]["emergency"][2]
            emergency_4 = team["lineup"]["bench"]["emergency"][3]
        except KeyError:
            continue

        if "captain" in team["lineup"]:
            captain = team["lineup"]["captain"]
        else:
            captain = ""
        if "vice_captain" in team["lineup"]:
            vice_captain = team["lineup"]["vice_captain"]
        else:
            vice_captain = ""

        value = team["value"]

        line = [round, team_id, user_id, team_name, overall_points, def_1, def_2, def_3, def_4, def_5,
         def_6, mid_1, mid_2, mid_3, mid_4, mid_5, mid_6, mid_7, mid_8, ruc_1, ruc_2, fwd_1,
         fwd_2, fwd_3, fwd_4, fwd_5, fwd_6, def_7, def_8, mid_9, mid_10, ruc_3, ruc_4, fwd_7,
         fwd_8, captain, vice_captain, emergency_1, emergency_2, emergency_3, emergency_4]

        with open(outputFile, "a") as output:
            writer = csv.writer(output)
            writer.writerow(line)