# Environment variable access for Cardbot

import dotenv, os

class CardEnv():
    def __init__(self):
        dotenv.load_dotenv() 
        self.server_token = os.getenv('DISCORD_TOKEN')
        self.server_id = os.getenv('DISCORD_GUILD')
        self.admin_role_id = os.getenv('DISCORD_ADMIN_ID')