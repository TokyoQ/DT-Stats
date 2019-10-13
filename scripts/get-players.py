import os
import requests
import json

endpoint = 'https://tds-afl-data.s3-ap-southeast-2.amazonaws.com/data/afl/players.json'

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = '{}/../data/raw'.format(script_dir)

output_filename = 'players.json'

raw = requests.get(endpoint)
with open('{}/{}'.format(output_dir, output_filename), 'wb') as f:
    f.write(raw.content)