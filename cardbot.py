# Cardbot - A bingo generator for Old School RuneScape

import commands, db, env, server 
import asyncio

class CardBot():
    def __init__(self):
        self.env = env.CardEnv()
        self.server = server.CardServer()
        self.bot = self.server.bot
        self.db = db.CardDatabase()
    
    async def register_commands(self) -> asyncio.coroutine:
        await cardbot.bot.add_cog(commands.CardCommands(self.db, self.bot))
           
    def start_bot(self):
        cardbot.bot.run(self.env.server_token)

if __name__ == "__main__":
    cardbot = CardBot()
    asyncio.run(cardbot.register_commands())
    cardbot.start_bot()