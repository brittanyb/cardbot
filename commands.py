# Discord commands for Cardbot

from discord.ext import commands
import discord
import random

class CardCommands(commands.Cog):
    def __init__(self, db, bot):
        self.db = db
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    async def create_table(self, ctx, table_name):
        if self.db.create_table(table_name):
            await ctx.send("Created item table with name - " + table_name)
            return
        await ctx.send("Could not create item table.")

    @commands.command()
    @commands.has_role("Admin")
    async def delete_table(self, ctx, table_name):
        if self.db.delete_table(table_name):
            await ctx.send("Deleted item table with name - " + table_name)
            return
        await ctx.send("Could not delete item table.")

    @commands.command()
    @commands.has_role("Admin")
    async def list_tables(self, ctx):
        table_str = self.db.list_tables()
        if table_str:
            await ctx.send("Available item tables - " + table_str)
            return
        await ctx.send("Could not list item tables.")

    @commands.command()
    @commands.has_role("Admin")
    async def add_item(self, ctx, table_name, item_name):
        if self.db.add_item(table_name, item_name):
            await ctx.send("Added item to table.")
            return
        await ctx.send("Could not add item to table.")

    @commands.command()
    @commands.has_role("Admin")
    async def delete_item(self, ctx, table_name, item_name):
        if self.db.delete_item(table_name, item_name):
            await ctx.send("Deleted item from table.")
            return
        await ctx.send("Could not delete item to table.")

    @commands.command()
    @commands.has_role("Admin")
    async def list_items(self, ctx, table_name):
        items = self.db.list_items(table_name)
        if items:
            item_str = ""
            for item in items:
                item_str += item[0] + ", "
            await ctx.send("Items in '" + table_name + "' table: " +  item_str)
            return
        await ctx.send("Could not list items.")

    @commands.command()
    @commands.has_role("Admin")
    async def start_competition(self, ctx):
        if self.db.create_competition():
            await ctx.send("Competition started!")
            return
        await ctx.send("Could not start competition.")

    @commands.command()
    @commands.has_role("Admin")
    async def end_competition(self, ctx):
        if self.db.delete_competition():
            await ctx.send("Competition ended!")
            return
        await ctx.send("Could not end competition.")

    @commands.command()
    @commands.has_role("Admin")
    async def add_points(self, ctx, user: discord.Member, points: int):
        user = user.id
        team_name, total_points = self.db.give_points(user, points)
        if team_name:
            await ctx.send(f"Gave {team_name} {points} points. They now have {total_points}!")
            return
        await ctx.send("Could not give points.")

    @commands.command()
    @commands.has_role("Admin")
    async def remove_points(self, ctx, user: discord.Member, points: int):
        user = user.id
        team_name, total_points = self.db.remove_points(user, points)
        if team_name:
            await ctx.send(f"Took {points} points from {team_name}. they now have {total_points} :(")
            return
        await ctx.send("Could not remove points.")

    @commands.command()
    @commands.has_role("Admin")
    async def verify_card(self, ctx, user: discord.Member, card_name):
        user = user.id
        team_name, points, total_points = self.db.verify_card(user, card_name)
        if points:
            await ctx.send(f"<@{user}> redeemed {card_name} for {points} points. {team_name} now have {total_points} points!")
            return
        await ctx.send("Could not verify card.")

    @commands.command()
    @commands.has_role("Admin")
    async def get_team_info(self, ctx, user: discord.Member):
        user = user.id
        team_info = self.db.get_team_info(user)
        if team_info:
            await ctx.send(team_info)
            return
        await ctx.send("Could not get team information.")
    
    @commands.command()
    @commands.has_role("Admin")
    async def remove_member(self, ctx, team_member: discord.Member):
        team_name = self.db.remove_member(team_member.id)
        if team_name:
            await ctx.send(f"{team_member} has been removed from {team_name}.")
            return
        await ctx.send("Could not remove team member.")

    @commands.command()
    @commands.has_role("Admin")
    async def redeem_card_sacrifice(self, ctx):
        if self.db.redeem_card_sacrifice():
            await ctx.send(f"One card has been added to team sacrifices.")
            return
        await ctx.send("Could not redeem card sacrifice.")

    @commands.command(pass_context=True)
    @commands.has_role("Team Leader")
    async def create_team(self, ctx, team_name):
        user = ctx.message.author.id
        if self.db.create_team(user, team_name):
            await ctx.send(f"<@{user}>'s team, {team_name} has joined the competition!")
            return
        await ctx.send("Could not create team.")

    @commands.command()
    @commands.has_role("Team Leader")
    async def create_team_invite(self, ctx, invited_user: discord.Member):
        user = ctx.message.author.id
        team_name = self.db.invite_user(user, invited_user.id)
        if team_name:
            await ctx.send(f"<@{invited_user.id}>, you have been invited to join {team_name}! To accept, type !accept_team_invite. To decline, type !decline_team_invite.")
            return
        await ctx.send("Could not invite user to join team.")

    @commands.command()
    @commands.has_role("Team Leader")
    async def reset_team_name(self, ctx, team_name):
        user = ctx.message.author.id
        team_name = self.db.reset_team_name(user, team_name)
        if team_name:
            await ctx.send(f"Your team's new name is now {team_name}")
            return
        await ctx.send("Could not reset team name.")

    @commands.command()
    async def accept_team_invite(self, ctx):
        user = ctx.message.author.id
        team_name = self.db.accept_invite(user)
        if team_name:
            await ctx.send(f"<@{user}> has joined {team_name}!")
            return
        await ctx.send(f"Could not join team.")

    @commands.command()
    async def decline_team_invite(self, ctx):
        user = ctx.message.author.id
        team_name = self.db.decline_invite(user)
        if team_name:
            await ctx.send(f"You didn't join {team_name} :(")
            return
        await ctx.send("Could not decline invite.")

    @commands.command()
    async def draw_card(self, ctx, tier):
        user = ctx.message.author.id
        team_name, card_name = self.db.draw_card(user, tier)
        if team_name:
            await ctx.send(f"{team_name}'s new card - {card_name}!")
            return
        await ctx.send("Could not draw card.")

    @commands.command()
    async def list_cards(self, ctx):
        user = ctx.message.author.id
        cards = self.db.list_cards(user)
        if cards:
            await ctx.send(cards)
            return
        await ctx.send("Could not list cards.")

    @commands.command()
    async def leaderboard(self, ctx):
        leaderboard = self.db.list_competitors()
        if leaderboard:
            await ctx.send(leaderboard)
            return
        await ctx.send("Could not list competitors.")

    @commands.command()
    async def list_team(self, ctx):
        user = ctx.message.author.id
        team = self.db.list_team(user)
        if team:
            await ctx.send(team)
            return
        await ctx.send("Could not list team.")

    @commands.command()
    async def sacrifice_card(self, ctx, card_name):
        user = ctx.message.author.id
        team_name = self.db.sacrifice_card(user, card_name)
        if team_name:
            await ctx.send(f"{team_name} have sacrificed their card - {card_name}")
            return
        await ctx.send("Could not sacrifice card.")

    # Temporary commands

    @commands.command()
    @commands.has_role("Admin")
    async def add_sacrifices(self, ctx):
        if self.db.add_sacrifices():
            await ctx.send(f"Added sacrifices.")
            return
        await ctx.send("Could not add sacrifices.")
    
    @commands.command()
    @commands.has_role("Admin")
    async def set_team_name(self, ctx, old_name, new_name):
        if self.db.set_team_name(old_name, new_name):
            await ctx.send(f"{old_name} reset to {new_name}")
            return
        await ctx.send("Could not update team name")

    @commands.command()
    @commands.has_role("Admin")
    async def admin_commands(self, ctx):
        adm_cmds = """```
Admin commands:
!create_table \"table_name\" -- Used to create an item table, e.g. an \"easy\" or \"medium\" table for potential item drops.
!delete_table \"table_name\" -- Deletes a previously created table.
!list_tables -- Lists all existing tables in the database.
!add_item \"table_name\" \"item_name\" -- Adds \"item_name\" to previously created \"table_name\", as a potential item drop.
!delete_item \"table_name\" \"item_name\" -- Deletes \"item_name\" from previous \"table_name\".
!list_items \"table_name\" -- Lists all currently added items on the \"table_name\" table.
!start_competition -- Starts up the competition database, and allows team leaders to create teams, and users to begin drawing cards.
!end_competition -- Stops the competition and WIPES ALL COMPETITION DATA.
!add_points @discord_user #points -- Gives a set number of #points to the team that @discord_user is in. For example, !add_points @Brittany 5
!remove_points @discord_user #points -- Removes a set number of #points from the team that @discord_user is in.
!verify_card @discord_user \"card_name\" -- Redeems an 'active' card from @discord_user's team, and moves it to the 'used' card deck. Redeems the cards points automatically.
!get_team_info @discord_user -- Lists the team of @discord_user, along with the points and cards.
!remove_member @discord_user -- Removes a user from their team.
!redeem_card_sacrifice -- Allows all teams to sacrifice a card from their deck.
```"""
        await ctx.send(adm_cmds)

    @commands.command()
    @commands.has_role("Team Leader")
    async def team_leader_commands(self, ctx):
        ldr_cmds = """```
Team Leader commands:
!create_team \"Team Name\" -- Used to create a team of up to 6 players for an ongoing competition.
!create_team_invite @discord_user -- Invites @discord_user to your team.
!reset_team_name \"Team Name\" -- Used to reset a team's name.
```"""
        await ctx.send(ldr_cmds)

    @commands.command()
    async def commands(self, ctx):
        cmds = """```
!accept_team_invite - Join a team that you have a pending invite for.
!decline_team_invite - Do not join the team that you have a pending invite for.
!draw_card \"tier\" - Draws a card from \"tier\" (e.g. easy, medium) table and adds it to the active deck of cards.
!list_cards - Lists all of your teams cards.
!sacrifice_card \"Card Name\" - When available, a card may be sacrificed from your active deck, so that a new card may be received.
!leaderboard - View all teams and their points.
!list_team - List the team that you are on, and their points.  
```"""
        await ctx.send(cmds)