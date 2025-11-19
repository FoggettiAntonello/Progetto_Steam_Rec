import chromadb
from chromadb.utils import embedding_functions
from typing import List
from src.config import Config


class VectorDB:
    """
    Gestisce indicizzazione e ricerca su ChromaDB.
    """

    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.CHROMA_PATH)

        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=Config.EMBEDDING_MODEL
        )

        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            embedding_function=self.embedding_fn
        )

    def index_documents(self, documents: List[str]):
        print(f"--- Indexing {len(documents)} documents ---")

        ids: List[str] = []
        docs: List[str] = []
        metas: List[dict] = []

        for i, d in enumerate(documents):
            ids.append(str(i))
            docs.append(d)

            cat_line = d.split("Genre/Genere: ")[1].split("\n")[0]
            en_cat, it_cat = cat_line.split(" | ")

            metas.append({
                "category": en_cat.lower(),
                "it_category": it_cat.lower(),
            })

        self.collection.upsert(
            documents=docs,
            ids=ids,
            metadatas=metas,
        )

    def search(self, query: str, k: int, category_hint: str | None = None) -> List[str]:
        where_clause = None

        if category_hint:
            c = category_hint.lower()
            where_clause = {
                "$or": [
                    {"category": {"$eq": c}},
                    {"it_category": {"$eq": c}},
                ]
            }

        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where_clause,
        )

        return results["documents"][0]
