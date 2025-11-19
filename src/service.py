from src.data_loader import SteamDataLoader
from src.vector_store import VectorDB
from src.rag_engine import RAGEngine
from src.config import Config

class SteamGameService:

    def __init__(self):
        self.loader = SteamDataLoader()
        self.vector_db = VectorDB()
        self.rag = RAGEngine()

    def refresh_database(self, category=None):
        cats = [category] if category else None
        raw = self.loader.fetch_data(cats)
        if raw:
            docs = self.loader.process_to_documents()
            self.vector_db.index_documents(docs)

    def query(self, question: str, lang: str = "auto"):
        if lang == "auto":
            lang = self.detect_lang(question)

        self.rag.set_language(lang)
        category_hint = self.extract_category(question)

        chunks = self.vector_db.search(
            question,
            k=Config.TOP_K_RETRIEVAL,
            category_hint=category_hint
        )

        return self.rag.generate_answer(question, chunks)

    @staticmethod
    def detect_lang(text: str) -> str:
        it_markers = ["qual", "miglior", "gioch", "categoria", "gdr"]
        return "it" if any(m in text.lower() for m in it_markers) else "en"

    def extract_category(self, text: str):
        text = text.lower()

        for cat in self.loader.default_categories:
            if cat.lower() in text:
                return cat

        for en, it in self.loader.tag_translations.items():
            if any(token in text for token in it.lower().split()):
                return en

        return None
