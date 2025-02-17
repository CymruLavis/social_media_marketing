import json
file_path = "C:\Users\Ethan Lavis\Desktop\keys.json"

class ProjectConfig():
    def __init__(self):
        with open(file_path, 'r') as f:
            keys = json.loads(f)
        self.IG_ACCESS_TOKEN = keys['access_token']
        self.IG_VERSION =  "v22.0"
        self.OPEN_AI_KEY = keys['open_ai_key']

settings = ProjectConfig()