import os
import json
file_path = os.path.join('trained_model.json')
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
with open(file_path, 'r') as json_file:
    recognizer = json.load(json_file)