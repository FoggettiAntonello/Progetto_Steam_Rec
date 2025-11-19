import argparse
from rich.console import Console
from rich.markdown import Markdown

from src.data_loader import SteamDataLoader
from src.vector_store import VectorDB
from src.rag_engine import RAGEngine
from src.config import Config

console = Console()


def detect_language(text: str) -> str:
    markers = ["qual", "miglior", "gioch", "categoria", "gdr", "calcio", "avventura"]
    return "it" if any(m in text.lower() for m in markers) else "en"


def extract_category(text: str, loader: SteamDataLoader):
    text = text.lower()

    for cat in loader.default_categories:
        if cat.lower() in text:
            return cat

    for en, it in loader.tag_translations.items():
        if any(tok in text for tok in it.lower().split()):
            return en

    return None


def filter_chunks_by_category(chunks, category_hint):
    if not category_hint:
        return chunks

    category_hint = category_hint.lower()
    filtered = []

    for ch in chunks:
        if "Genre/Genere:" not in ch:
            continue

        line = ch.split("Genre/Genere: ")[1].split("\n")[0]
        en_cat, it_cat = line.split(" | ")

        if en_cat.lower() == category_hint or it_cat.lower() == category_hint:
            filtered.append(ch)

    return filtered if filtered else chunks


def main():
    parser = argparse.ArgumentParser(description="Steam RAG App ⭐ YAML Enabled")
    parser.add_argument("--query", type=str)
    parser.add_argument("--category", type=str)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--lang", type=str, default="auto")
    args = parser.parse_args()

    loader = SteamDataLoader()
    vector_db = VectorDB()
    rag = RAGEngine()

    if args.refresh or args.category:
        cats = [args.category] if args.category else None
        raw = loader.fetch_data(cats)

        if raw:
            docs = loader.process_to_documents()
            vector_db.index_documents(docs)

    query = args.query or input(
        "⭐ Scrivi una domanda sui videogiochi (es: migliori roguelike): "
    )

    lang = detect_language(query) if args.lang == "auto" else args.lang
    rag.set_language(lang)

    category_hint = extract_category(query, loader)

    raw_chunks = vector_db.search(query, k=Config.TOP_K, category_hint=category_hint)
    chunks = filter_chunks_by_category(raw_chunks, category_hint)

    answer = rag.generate_answer(query, chunks)

    console.print("\n[bold cyan]🎮 RISPOSTA DEL SISTEMA[/bold cyan]\n")
    console.print(Markdown(answer))


if __name__ == "__main__":
    main()
