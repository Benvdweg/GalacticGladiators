import random
from models.player_model import PlayerModel


class PlayerDAO:
    def __init__(self, cnx):
        self.cnx = cnx

    def create_players_for_game(self, nickname, game_id):
        cursor = self.cnx.cursor()
        query = "INSERT INTO players (nickname, game_id, is_bot) VALUES (%s, %s, FALSE)"
        cursor.execute(query, (nickname, game_id))
        self.cnx.commit()

        enemy_nicknames = [
            "Darth Oblivion", "Lord Ragnarok", "Emperor Darkstar", "Supreme Overlord Nexus",
            "Baron Blackhole", "Commander Void", "Warlord Eclipse", "General Doomstar",
            "Empress Malefica", "Count Nihilus", "Duchess Malevolence",
            "Prince Vortex", "Sir Devastator", "General Doomfist", "General Grievous",
            "Galactus", "Count Darklight", "Prince Meteor", "Sephiroth", "Supreme Emperor Void",
            "The Devourer of Worlds", "The Cosmic Tyrant", "Emperor Infinity", "Erwin 'Kingslayer' Goud",
            "Chris 'God' Guilliamse", "Lord Dongmin"
        ]

        bot_nickname = random.choice(enemy_nicknames)

        query = "INSERT INTO players (nickname, game_id, is_bot) VALUES (%s, %s, TRUE)"
        cursor.execute(query, (bot_nickname, game_id))
        self.cnx.commit()

        enemy_id = cursor.lastrowid

        cursor.close()

        return enemy_id

    def get_players(self, game_id):
        cursor = self.cnx.cursor()
        query = ("SELECT player_id, nickname, is_bot, score, game_id FROM players WHERE "
                 "game_id = %s")
        cursor.execute(query, (game_id,))
        players_data = cursor.fetchall()
        cursor.close()

        player = None
        enemy_player = None

        for row in players_data:
            current_player = PlayerModel(*row)
            if current_player.is_bot:
                enemy_player = current_player
            else:
                player = current_player

        return player, enemy_player

    def update_score(self, score, game_id, is_bot):
        cursor = self.cnx.cursor()
        query = "UPDATE players SET score = score + %s WHERE game_id = %s AND is_bot = %s"
        cursor.execute(query, (score, game_id, is_bot))
        self.cnx.commit()
        cursor.close()

    def add_gold(self, player_id):
        cursor = self.cnx.cursor()
        query = "UPDATE players SET score = score + 1 WHERE player_id = %s"
        cursor.execute(query, (player_id,))
        self.cnx.commit()
        cursor.close()
