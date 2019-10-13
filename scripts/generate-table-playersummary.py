import os
import json
import csv

# Parameters
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = '{}/../data/raw'.format(script_dir)
input_filename = 'players.json'
output_dir = '{}/../data/normalised'.format(script_dir)
output_filename = 'player_summary.csv'

header = ['id', 'first_name', 'last_name', 'games_played', 'total_points',
    'avg_points', 'high_score', 'low_score', 'final_cost', 'final_selections',
    'is_def', 'is_mid', 'is_ruc', 'is_fwd']

# MAIN
input_file = open('{}/{}'.format(input_dir, input_filename), 'rb')
players = json.loads(input_file.read())

with open('{}/{}'.format(output_dir, output_filename), "w") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)
    for player in players:
        id = player['id']
        first_name = player['first_name']
        last_name = player['last_name']

        stats = player['stats']
        games_played = stats['games_played']
        total_points = stats['total_points']
        avg_points = stats['avg_points']
        high_score = stats['high_score']
        low_score = stats['low_score']
        final_cost = player['cost']
        final_selections = stats['selections']
        final_ownership = stats['owned_by']

        positions = player['positions']
        is_def = 1 in positions
        is_mid = 2 in positions
        is_ruc = 3 in positions
        is_fwd = 4 in positions

        row = [id, first_name, last_name, games_played, total_points,
            avg_points, high_score, low_score, final_cost, final_selections,
            is_def, is_mid, is_ruc, is_fwd]
        #print(row)
        writer.writerow(row)
