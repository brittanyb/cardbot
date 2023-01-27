# Database API for Cardbot

import sqlite3
import random

class CardDatabase():
    def __init__(self):
        self.db = sqlite3.connect("cards.db")
        self.db_cursor = self.db.cursor()

    def create_table(self, table_name):
        try:
            self.db_cursor.execute("CREATE TABLE " + table_name + "(item)")
            return True
        except Exception as e:
            return False

    def delete_table(self, table_name):
        try:
            self.db_cursor.execute("DROP TABLE " + table_name)
            return True
        except Exception as e:
            return False

    def list_tables(self):
        try:
            self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = self.db_cursor.fetchall()
        except Exception as e:
            return False   
        if not tables:
            return False
        else:
            table_str = ""
            for table in tables:
                table_str += table[0] + ", "
            return table_str

    def add_item(self, table_name, item_name):
        try:
            self.db_cursor.execute("INSERT INTO " + table_name + "(item) VALUES (\"" + item_name + "\")")
            self.db.commit()
            return True
        except Exception as e:
            return False

    def delete_item(self, table_name, item_name):
        try:
            self.db_cursor.execute("DELETE FROM " + table_name + " WHERE item = \"" + item_name + "\"")
            self.db.commit()
            return True
        except Exception as e:
            return False
    
    def list_items(self, table_name):
        try:
            self.db_cursor.execute("SELECT * FROM " + table_name)
            items = self.db_cursor.fetchall()
        except Exception as e:
            return False
        if not items:
            return False
        else:
            return items

    def create_competition(self):
        try:
            self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='competition'")
            competition = self.db_cursor.fetchall()
            self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invitations'")
            invitations = self.db_cursor.fetchall()
            self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cards'")
            cards = self.db_cursor.fetchall()
            if competition or invitations or cards:
                return False
            self.db_cursor.execute("CREATE TABLE competition (team_name, points, user1, user2, user3, user4, user5, user6, sacrifices)")
            self.db_cursor.execute("CREATE TABLE invitations (team_name, invite1, invite2, invite3, invite4, invite5)")
            self.db_cursor.execute("CREATE TABLE cards (team_name, active_card1, active_card2, active_card3, active_card4, active_card5, used_card1, used_card2, used_card3, used_card4, used_card5, used_card6, used_card7, used_card8, used_card9, used_card10, used_card11, used_card12, used_card13, used_card14, used_card15)")
            return True
        except Exception as e:
            return False

    def delete_competition(self):
        try:
            self.db_cursor.execute("DROP TABLE competition")
            self.db_cursor.execute("DROP TABLE invitations")
            self.db_cursor.execute("DROP TABLE cards")
            return True
        except Exception as e:
            return False

    def create_team(self, user, team_name):
        try:
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ?", (user,))
            user_exists = self.db_cursor.fetchall()
            if user_exists:
                return False
            self.db_cursor.execute("SELECT * FROM competition where team_name = ?", (team_name,))
            team_name_exists = self.db_cursor.fetchall()
            if team_name_exists:
                return False
            team_values = [team_name, 0, user, 'None', 'None', 'None', 'None', 'None', 'None']
            invitation_values = [team_name, 'None', 'None', 'None', 'None', 'None']
            card_values = [team_name, 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None']
            self.db_cursor.execute("INSERT INTO competition VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", team_values)
            self.db_cursor.execute("INSERT INTO invitations VALUES (?, ?, ?, ?, ?, ?)", invitation_values)
            self.db_cursor.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", card_values)
            self.db.commit()
            return True
        except Exception as e:
            return False

    def invite_user(self, team_leader, invitee):
        try:
            # Get current team member count
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ?", (team_leader,))
            team_values = self.db_cursor.fetchall()
            print(f"invite_user: competition db - {team_values}")
            if not team_values:
                return False
            team_count = 0
            team_members = team_values[0][2:8]
            for team_member in team_members:
                if team_member != 'None':
                    team_count += 1
            # Get if user is already part of another team
            team_name = team_values[0][0]
            self.db_cursor.execute("SELECT * FROM competition", (team_name,))
            other_teams = self.db_cursor.fetchall()
            print(f"invite_user: other competitors db - {other_teams}")
            if invitee in other_teams:
                return False
            print(f"invite_user: User not in other team")
            # Get if user has a pending invitation already
            self.db_cursor.execute("SELECT * FROM invitations")
            all_invite_values = self.db_cursor.fetchall()
            for invites in all_invite_values:
                team_invites = invites[1:6]
                if invitee in team_invites:
                    return False
            print(f"invite_user: No other pending invites.")
            # Get whether user can fit on the team/invite list
            self.db_cursor.execute("SELECT * FROM invitations WHERE team_name = ?", (team_name,))
            invite_values = self.db_cursor.fetchall()
            team_invites = invite_values[0][1:6]
            invite_count = 0
            for invite in team_invites:
                if invite != 'None':
                    invite_count += 1
            if ((team_count + invite_count) > 5):
                return False
            if (invite_count > 4):
                return False
            print(f"invite_user: User counts acceptable")
            # Build the invite list with the user in it
            new_invite_values = ['None'] * 6
            invite_set = False
            for index, invite in enumerate(team_invites):
                if invite == 'None' and invite_set == False:
                    new_invite_values[index] = invitee
                    invite_set = True
                else:
                    new_invite_values[index] = team_invites[index]
            new_invite_values[5] = team_name
            print(f"invite_user: Invite list rebuilt - {new_invite_values}")
            self.db_cursor.execute("UPDATE invitations SET invite1 = ?, invite2 = ?, invite3 = ?, invite4 = ?, invite5 = ? WHERE team_name = ?", new_invite_values)
            self.db.commit()
            return team_name
        except Exception as e:
            print(f"invite_user: ERROR - {e}")
            return False

    def reset_team_name(self, user, new_team_name):
        try:
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ?", (user,))
            team_values = self.db_cursor.fetchall()
            team_name = team_values[0][0]
            db_values = [new_team_name, team_name]
            self.db_cursor.execute("UPDATE competition SET team_name = ? WHERE team_name = ?", db_values)
            self.db.commit()
            return new_team_name
        except Exception as e:
            print(f"reset_team_name: ERROR - {e}")
            return False

    def remove_member(self, user):
        try:
            self.db_cursor.execute("SELECT * FROM competition WHERE user2 = ? OR user3 = ? OR user4 = ? OR user5 = ? OR user6 = ?", (user, user, user, user, user))
            team_values = self.db_cursor.fetchall()
            print(team_values)
            team_name = team_values[0][0]
            team_members = team_values[0][2:8]
            new_team_members = ['None'] * 6
            for index, invite in enumerate(team_members):
                new_team_members[index] = team_members[index]
            print("enumerated team members")
            member_removed = False
            for index, member in enumerate(new_team_members):
                if member == user and member_removed == False:
                    new_team_members.pop(index)
                    member_removed = True
            new_team_members.append('None')
            new_team_members.append(team_name)
            print(f"remove_member: {new_team_members}")
            self.db_cursor.execute("UPDATE competition SET user1 = ?, user2 = ?, user3 = ?, user4 = ?, user5 = ?, user6 = ? WHERE team_name = ?", new_team_members)
            self.db.commit()
        except Exception as e:
            print(f"remove_member: ERROR - {e}")
            return False

    def accept_invite(self, user):
        try:
            # Is the user invited to join the team?
            print(f"accept_invite: {user} invokes.")
            self.db_cursor.execute("SELECT * FROM invitations WHERE invite1 = ? OR invite2 = ? OR invite3 = ? OR invite4 = ? OR invite5 = ?", (user, user, user, user, user))
            invite_values = self.db_cursor.fetchall()
            team_name = invite_values[0][0]
            team_invites = invite_values[0][1:6]
            user_invited = False
            for invite in team_invites:
                if invite == user:
                    user_invited = True
            if user_invited == False:
                return False
            print(f"accept_invite: invitation db - {invite_values}")
            print(f"accept_invite: Checks passed to join {team_name}")
            # Re-build the invite list
            new_team_invites = ['None'] * 5
            for index, invite in enumerate(team_invites):
                new_team_invites[index] = team_invites[index]
            user_found = False
            for index, invite in enumerate(new_team_invites):
                if invite == user and user_found == False:
                    new_team_invites.pop(index)
                    user_found = True
            new_team_invites.append('None')
            new_team_invites.append(team_name)
            print(f"accept_invite: Invite list rebuilt - {new_team_invites}")
            # Re-build the team list
            self.db_cursor.execute("SELECT * FROM competition WHERE team_name = ?", (team_name,))
            team_values = self.db_cursor.fetchall()
            print(f"accept_invite: competition db - {team_values}")
            team_members = team_values[0][2:8]
            new_team_members = ['None'] * 6
            for index, team_member in enumerate(team_members):
                new_team_members[index] = team_members[index]
            user_added = False
            for index, team_member in enumerate(new_team_members):
                if team_member == 'None' and user_added == False:
                    new_team_members[index] = user
                    user_added = True
            new_team_members.append(team_name)
            print(f"accept_invite: Team list rebuilt - {new_team_members}")
            # Update the database entries
            self.db_cursor.execute("UPDATE invitations SET invite1 = ?, invite2 = ?, invite3 = ?, invite4 = ?, invite5 = ? WHERE team_name = ?", new_team_invites)
            self.db_cursor.execute("UPDATE competition SET user1 = ?, user2 = ?, user3 = ?, user4 = ?, user5 = ?, user6 = ? WHERE team_name = ?", new_team_members)
            self.db.commit()
            return team_name
        except Exception as e:
            print(f"accept_invite: ERROR - {e}")
            return False

    def decline_invite(self, user):
        try:
            # Is the user invited to join the team?
            self.db_cursor.execute("SELECT * FROM invitations WHERE invite1 = ? OR invite2 = ? OR invite3 = ? OR invite4 = ? OR invite5 = ?", (user, user, user, user, user))
            invite_values = self.db_cursor.fetchall()
            team_name = invite_values[0][0]
            team_invites = invite_values[0][1:6]
            user_invited = False
            for invite in team_invites:
                if invite == user:
                    user_invited = True
            if user_invited == False:
                return False
            # Re-build the invite list
            new_team_invites = ['None'] * 5
            for index, invite in enumerate(team_invites):
                new_team_invites[index] = team_invites[index]
            user_found = False
            for index, invite in enumerate(new_team_invites):
                if invite == user and user_found == False:
                    new_team_invites.pop(index)
                    user_found = True
            new_team_invites.append('None')
            new_team_invites.append(team_name)
            self.db_cursor.execute("UPDATE invitations SET invite1 = ?, invite2 = ?, invite3 = ?, invite4 = ?, invite5 = ? WHERE team_name = ?", new_team_invites)
            self.db.commit()
            return team_name
        except Exception as e:
            return False

    def list_competitors(self):
        try:
            self.db_cursor.execute("SELECT * FROM competition ORDER BY POINTS DESC")
            scores = self.db_cursor.fetchall()
            competition_str = "```\n"
            for score in scores:
                competition_str += f"{score[0]} - {score[1]} points\n"
            competition_str += "```\n"
            return competition_str
        except Exception as e:
            return False

    def redeem_card_sacrifice(self):
        try:
            self.db_cursor.execute("SELECT * FROM competition")
            team_values = self.db_cursor.fetchall()
            for team in team_values:
                team_name = team[0]
                card_sacrifice = team[8] + 1
                values = [card_sacrifice, team_name]
                self.db_cursor.execute("UPDATE competition SET sacrifices = ? WHERE team_name = ?", values)
                self.db.commit()
            return True
        except Exception as e:
            print(f"redeem_card_sacrifice: ERROR - {e}")
            return False

    def add_sacrifices(self):
        try:
            self.db_cursor.execute("ALTER TABLE competition ADD sacrifices DEFAULT -2")
            self.db.commit()
            return True
        except Exception as e:
            print(f"add_sacrifices: ERROR - {e}")
            return False

    def sacrifice_card(self, user, card_name):
        try:
            print("sacrifice_card")
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                print("No team values")
                return False
            team_name = team_values[0][0]
            sacrifices = team_values[0][8]
            print(f"Team found: {team_name}, Sacrifices: {sacrifices}")
            if sacrifices <= 0:
                print("No sacrifices.")
                return False
            sacrifices = sacrifices - 1
            self.db_cursor.execute("SELECT * FROM cards WHERE team_name = ?", (team_name,))
            cards = self.db_cursor.fetchall()
            active_cards = cards[0][1:6]
            card_found = False
            new_active_cards = list(active_cards)
            for index, card in enumerate(new_active_cards):
                if card == card_name and card_found == False:
                    new_active_cards.pop(index)
                    card_found = True
            if card_found == False:
                print("Card not found")
                return False
            new_active_cards.append('None')
            new_active_cards.append(team_name)
            self.db_cursor.execute("UPDATE cards SET active_card1 = ?, active_card2 = ?, active_card3 = ?, active_card4 = ?, active_card5 = ? WHERE team_name = ?", new_active_cards)
            self.db.commit()
            return team_name
        except Exception as e:
            print(f"sacrifice_card: ERROR - {e}")
            return False

    def give_points(self, user, points):
        try:
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                return False, False
            team_name = team_values[0][0]
            team_points = team_values[0][1]
            new_team_points = team_points + points
            values = [new_team_points, team_name]
            self.db_cursor.execute("UPDATE competition SET points = ? where team_name = ?", values)
            self.db.commit()
            return team_name, new_team_points
        except Exception as e:
            return False, False
        
    def remove_points(self, user, points):
        try:
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                return False, False
            team_name = team_values[0][0]
            team_points = team_values[0][1]
            new_team_points = team_points - points
            values = [new_team_points, team_name]
            self.db_cursor.execute("UPDATE competition SET points = ? where team_name = ?", values)
            self.db.commit()
            return team_name, new_team_points
        except Exception as e:
            return False, False

    def draw_card(self, user, tier):
        try:
            # Get the users team
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                return False, False
            # Get teams active and used cards
            team_name = team_values[0][0]
            self.db_cursor.execute("SELECT * FROM cards WHERE team_name = ?", (team_name,))
            card_values = self.db_cursor.fetchall()
            active_cards = card_values[0][1:6]
            used_cards = card_values[0][6:21]
            all_cards = card_values[0][1:21]
            active_card_count = 0
            for card in active_cards:
                if card != 'None':
                    active_card_count += 1
            used_card_count = 0
            for card in  used_cards:
                if card != 'None':
                    used_card_count += 1
            if (active_card_count + used_card_count > 14):
                return False, False
            if (active_card_count > 4):
                return False, False
            # Get whether the tier is exhausted of entries
            items = self.list_items(tier)
            items = [x[0] for x in items]
            available_items = [x for x in items if x not in all_cards]
            if not available_items:
                return False, False
            row_number = random.randint(0,len(available_items)-1)
            card_name = available_items[row_number]
            # Add the card to the active deck
            new_active_cards = list(active_cards)
            card_added = False
            for index, card in enumerate(active_cards):
                if card == 'None' and card_added == False:
                    new_active_cards[index] = card_name
                    card_added = True
            new_active_cards.append(team_name)
            self.db_cursor.execute("UPDATE cards SET active_card1 = ?, active_card2 = ?, active_card3 = ?, active_card4 = ?, active_card5 = ? WHERE team_name = ?", new_active_cards)
            self.db.commit()
            return team_name, card_name
        except Exception as e:
            return False, False

    def verify_card(self, user, card_name):
        try:
            # Get users team
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                return False, False, False
            # Determine whether the card is active
            team_name = team_values[0][0]
            self.db_cursor.execute("SELECT * FROM cards WHERE team_name = ?", (team_name,))
            cards = self.db_cursor.fetchall()
            active_cards = cards[0][1:6]
            if card_name not in active_cards:
                return False, False, False
            # Get the points for the card
            easy = [x[0] for x in self.list_items('easy')]
            medium = [x[0] for x in self.list_items('medium')]
            hard = [x[0] for x in self.list_items('hard')]
            elite = [x[0] for x in self.list_items('elite')]
            grandmaster = [x[0] for x in self.list_items('grandmaster')]
            points = 0
            if card_name in easy:
                points = 1
            elif card_name in medium:
                points = 3
            elif card_name in hard:
                points = 5
            elif card_name in elite:
                points = 8
            elif card_name in grandmaster:
                points = 10
            else:
                return False, False, False
            # Give the users team some points
            team_points = team_values[0][1]
            new_team_points = team_points + points
            values = [new_team_points, team_name]
            self.db_cursor.execute("UPDATE competition SET points = ? where team_name = ?", values)
            # Move the card from active to used
            card_found = False
            new_active_cards = list(active_cards)
            for index, card in enumerate(new_active_cards):
                if card == card_name and card_found == False:
                    new_active_cards.pop(index)
                    card_found = True
            new_active_cards.append('None')
            new_active_cards.append(team_name)
            self.db_cursor.execute("UPDATE cards SET active_card1 = ?, active_card2 = ?, active_card3 = ?, active_card4 = ?, active_card5 = ? WHERE team_name = ?", new_active_cards)
            new_used_cards = list(cards[0][6:21])
            card_added = False
            for index, card in enumerate(new_used_cards):
                if card == 'None' and card_added == False:
                    new_used_cards[index] = card_name
                    card_added = True
            new_used_cards.append(team_name)
            self.db_cursor.execute("UPDATE cards SET used_card1 = ?, used_card2 = ?, used_card3 = ?, used_card4 = ?, used_card5 = ?, used_card6 = ?, used_card7 = ?, used_card8 = ?, used_card9 = ?, used_card10 = ?, used_card11 = ?, used_card12 = ?, used_card13 = ?, used_card14 = ?, used_card15 = ? WHERE team_name = ?", new_used_cards)
            self.db.commit()
            return team_name, points, new_team_points
        except Exception as e:
            return False, False, False

    def list_cards(self, user):
        try:
            # Get users team
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                return False
            # Get teams cards
            team_name = team_values[0][0]
            self.db_cursor.execute("SELECT * FROM cards WHERE team_name = ?", (team_name,))
            card_values = self.db_cursor.fetchall()
            # Create response
            response_str = f"```\n{team_name}'s Cards:\n"
            for index, card in enumerate(card_values[0][1:6]):
                response_str += f"Active card {index + 1}: {card}\n"
            for index, card in enumerate(card_values[0][6:21]):
                response_str += f"Redeemed card {index + 1}: {card}\n"
            response_str += "```\n"
            return response_str
        except Exception as e:
            return False
    
    def list_team(self, user):
        try:
            users = [user] * 6
            self.db_cursor.execute("SELECT * FROM competition WHERE user1 = ? or user2 = ? or user3 = ? or user4 = ? or user5 = ? or user6 = ?", users)
            team_values = self.db_cursor.fetchall()
            if not team_values:
                return False
            team_name = team_values[0][0]
            team_str = f"{team_name} members: \n"
            for member in team_values[0][2:8]:
                if member != 'None':
                    team_str += f"<@{member}>\n"
            team_str += f"Points - {team_values[0][1]}\n"
            team_str += f"Card Sacrifices Left - {team_values[0][8]}\n"
            return team_str
        except Exception as e:
            print(e)
            return False

    def get_team_info(self, user):
        team_info_str = ""
        team_info = self.list_team(user)
        if not team_info:
            return False
        cards_info = self.list_cards(user)
        if not cards_info:
            return False
        team_info_str += team_info
        team_info_str += cards_info
        return team_info_str