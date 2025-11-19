import argparse
from rich.console import Console
from rich.markdown import Markdown

from src.data_loader import SteamDataLoader
from src.vector_store import VectorDB
from src.rag_engine import RAGEngine
from src.config import Config


console = Console()


def detect_language(text: str) -> str:
    """Riconoscimento semplice ed efficace della lingua."""
    it_markers = ["qual", "miglior", "gioch", "categoria", "gdr", "calcio", "avventura"]
    return "it" if any(w in text.lower() for w in it_markers) else "en"


def extract_category(text: str, loader: SteamDataLoader):
    """Estrae la categoria richiesta dall’utente."""
    text = text.lower()

    # Cerca categorie inglesi
    for cat in loader.default_categories:
        if cat.lower() in text:
            return cat

    # Cerca categorie italiane
    for en, it in loader.tag_translations.items():
        if any(token in text for token in it.lower().split()):
            return en

    return None


def filter_chunks_by_category(chunks, category_hint):
    """
    Filtraggio Python dei chunk per rimuovere quelli con categorie sbagliate.
    Ad esempio: Bowling Roguelike → eliminato.
    """

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

    # Fallback per evitare crash: se nessun gioco è valido, usa comunque i chunk
    return filtered if filtered else chunks


def main():
    parser = argparse.ArgumentParser(description="Steam RAG App ⭐ App-ready Edition")
    parser.add_argument("--query", type=str)
    parser.add_argument("--category", type=str)
    parser.add_argument("--temp", type=float, default=Config.DEFAULT_TEMPERATURE)
    parser.add_argument("--lang", type=str, default="auto", choices=["auto", "it", "en"])
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    # Pipeline di base
    loader = SteamDataLoader()
    vector_db = VectorDB()
    rag = RAGEngine()

    # Refresh database
    if args.refresh or args.category:
        cats = [args.category] if args.category else None
        raw = loader.fetch_data(cats)

        if raw:
            docs = loader.process_to_documents()
            vector_db.index_documents(docs)

    # Richiesta utente
    query = args.query or input(
        "⭐ Scrivi una domanda sui videogiochi (es: migliori roguelike): "
    )

    # Lingua
    lang = detect_language(query) if args.lang == "auto" else args.lang
    rag.set_language(lang)

    # Categoria filtraggio
    category_hint = extract_category(query, loader)

    # Recupero chunk dal DB
    raw_chunks = vector_db.search(
        query,
        k=Config.TOP_K_RETRIEVAL,
        category_hint=category_hint
    )

    # Filtraggio intelligente
    chunks = filter_chunks_by_category(raw_chunks, category_hint)

    # Risposta LLM
    answer = rag.generate_answer(query, chunks)

    # Output elegante
    console.print("\n[bold cyan]🎮 RISPOSTA DEL SISTEMA[/bold cyan]\n")
    console.print(Markdown(answer))


if __name__ == "__main__":
    main()
