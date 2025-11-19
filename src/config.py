import os
import yaml


class Config:
    """
    Configurazione globale del progetto.
    Legge da config.yaml (root del progetto) e popola ATTRIBUTI DI CLASSE,
    così possono essere usati come Config.X ovunque.
    """

    # Valori di default (se manca il file YAML o qualche chiave)
    MODEL_NAME: str = "llama3"
    TEMPERATURE: float = 0.0
    DEFAULT_TEMPERATURE: float = 0.0

    CHROMA_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "steam_games"
    TOP_K: int = 12

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    DEFAULT_CATEGORIES = [
        "FPS", "RPG", "Strategy", "Simulation", "Action",
        "Fighting", "Sports", "Racing", "Horror", "Indie",
        "Adventure", "Open World", "Puzzle", "Sci-fi", "Co-op",
        "Multiplayer", "Survival", "Battle Royale", "MMORPG",
        "Platformer", "Roguelike", "Roguelite", "Metroidvania",
        "Soulslike", "Card Game", "Soccer", "Football", "Basketball",
    ]

    TAG_TRANSLATIONS = {
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
        "Card Game": "Gioco di carte",
    }

    DEFAULT_LANGUAGE: str = "auto"
    FANCY_CLI: bool = True

    @classmethod
    def load_from_yaml(cls, path: str | None = None) -> None:
        """
        Carica config.yaml (se esiste) e sovrascrive i default.
        """
        if path is None:
            path = os.path.join(os.getcwd(), "config.yaml")

        if not os.path.exists(path):
            # Nessun YAML -> usiamo i default senza errori
            return

        with open(path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        # MODEL
        model_cfg = cfg.get("model", {})
        cls.MODEL_NAME = model_cfg.get("ollama_model", cls.MODEL_NAME)
        cls.TEMPERATURE = model_cfg.get("temperature", cls.TEMPERATURE)
        cls.DEFAULT_TEMPERATURE = cls.TEMPERATURE  # alias comodo

        # DATABASE
        db_cfg = cfg.get("database", {})
        cls.CHROMA_PATH = db_cfg.get("chroma_path", cls.CHROMA_PATH)
        cls.TOP_K = db_cfg.get("top_k", cls.TOP_K)

        # CATEGORIES
        cat_cfg = cfg.get("categories", {})
        cls.DEFAULT_CATEGORIES = cat_cfg.get("default", cls.DEFAULT_CATEGORIES)

        # TRADUZIONI
        cls.TAG_TRANSLATIONS = cfg.get("translations", cls.TAG_TRANSLATIONS)

        # APP
        app_cfg = cfg.get("app", {})
        cls.DEFAULT_LANGUAGE = app_cfg.get("default_language", cls.DEFAULT_LANGUAGE)
        cls.FANCY_CLI = app_cfg.get("fancy_cli", cls.FANCY_CLI)


# Carica YAML all'import del modulo
Config.load_from_yaml()
