import requests
import time
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SteamDataLoader:
    def __init__(self):
        self.raw_data = []
        self.base_url = "https://steamspy.com/api.php"
        
        self.default_categories = [
            "FPS", "RPG", "Strategy", "Simulation", "Action",
            "Fighting", "Sports", "Racing", "Horror", "Indie",
            "Adventure", "Open World", "Puzzle", "Sci-fi", "Co-op",
            "Multiplayer", "Survival", "Battle Royale", "MMORPG",
            "Platformer", "Roguelike", "Roguelite", "Metroidvania",
            "Soulslike", "Card Game", "Soccer", "Football",
            "Basketball"
        ]
        
        self.tag_translations = {
            "FPS": "Sparatutto in prima persona",
            "RPG": "Gioco di ruolo",
            "Strategy": "Strategia",
            "Simulation": "Simulazione",
            "Action": "Azione",
            "Fighting": "Picchiaduro",
            "Sports": "Sportivo",
            "Racing": "Corse",
            "Horror": "Orrore",
            "Adventure": "Avventura",
            "Survival": "Sopravvivenza",
            "Soccer": "Calcio",
            "Football": "Calcio",
            "Roguelike": "Roguelike",
            "Roguelite": "Roguelite",
            "Card Game": "Gioco di carte"
        }

    def fetch_data(self, target_categories: List[str] = None) -> List[Dict]:
        categories_to_fetch = target_categories if target_categories else self.default_categories
        
        print(f"--- [Extract] Fetching categories: {categories_to_fetch} ---")
        all_games = {}

        for category in categories_to_fetch:
            print(f"   -> Tag: {category}")
            try:
                url = f"{self.base_url}?request=tag&tag={category}"
                response = requests.get(url)

                if response.status_code != 200:
                    continue

                data = response.json()
                if not data:
                    continue

                sorted_games = sorted(
                    data.values(),
                    key=lambda x: x.get("ccu", 0),
                    reverse=True
                )[:30]

                for game in sorted_games:
                    appid = game.get("appid")
                    if not appid:
                        continue

                    it_tag = self.tag_translations.get(category, category)

                    if appid not in all_games:
                        all_games[appid] = {
                            "name": game.get("name"),
                            "category": category,
                            "it_category": it_tag,
                            "ccu": game.get("ccu", 0),
                            "owners": game.get("owners", "N/A"),
                            "userscore": game.get("userscore", 0),
                            "developer": game.get("developer", "Unknown"),
                            "price": game.get("price", "0"),
                            "description": (
                                f"Category: {category} / {it_tag}. "
                                f"Developer: {game.get('developer')}. "
                                f"Active players: {game.get('ccu')}. "
                                f"Score: {game.get('userscore')}/100."
                            )
                        }
                    else:
                        all_games[appid]["description"] += f" Also tagged: {category}."

                time.sleep(1)

            except Exception as e:
                logger.error(f"Error: {e}")

        self.raw_data = list(all_games.values())
        print(f"--- Extracted {len(self.raw_data)} games ---")
        return self.raw_data

    def process_to_documents(self) -> List[str]:
        docs = []

        for item in self.raw_data:
            try:
                price_val = float(item["price"]) / 100
                price = "Free" if price_val == 0 else f"{price_val:.2f}$"
            except:
                price = "N/A"

            text = (
                f"Game: {item['name']}\n"
                f"Genre/Genere: {item['category']} | {item['it_category']}\n"
                f"CCU: {item['ccu']}\n"
                f"Owners: {item['owners']}\n"
                f"Description: {item['description']}\n"
                f"Price: {price}"
            )

            docs.append(text)

        return docs
