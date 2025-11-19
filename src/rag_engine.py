import ollama
from typing import List
from src.config import Config


class RAGEngine:
    def __init__(self, model_name: str = Config.OLLAMA_MODEL, language: str = "auto"):
        self.model_name = model_name
        self.language = language

        # Prompt sistemico robusto e API-friendly
        self.base_prompt = """
You are a deterministic Steam game database assistant.
You must follow these strict rules:

1. LANGUAGE:
   Respond strictly in: {LANG}. Never mix languages.

2. FILTERING:
   Only output games whose "Genre/Genere" matches the category requested.
   Never invent titles. Only use items present in CONTEXT DATA.

3. NO MATCHES:
   If no valid games exist, output exactly:
   "Nessun gioco trovato per questa categoria specifica".

4. FORMAT:
   Provide EXACTLY 5 bullet points.
   Format each as:
   **NAME** – CCU – short description.

5. OUTPUT:
   Your final answer MUST be clean, structured, and in Markdown.
"""

    def set_language(self, lang: str):
        self.language = lang

    def generate_answer(self, query: str, context_chunks: List[str]) -> str:
        """
        Genera una risposta formattata in Markdown.
        Perfetta per interfaccia grafica o API.
        """

        prompt = self.base_prompt.replace("{LANG}", self.language)
        context = "\n\n".join(context_chunks)

        user_prompt = (
            f"{prompt}\n\n"
            f"### 📘 CONTEXT DATA\n"
            f"{context}\n\n"
            f"### ❓ USER QUESTION\n"
            f"{query}\n\n"
            f"### 🧠 TASK\n"
            f"Produce una risposta pulita, formattata, senza aggiungere testo superfluo."
        )

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={"temperature": 0.0}
            )

            return response["message"]["content"].strip()

        except Exception as e:
            return f"⚠️ Errore di connessione a Ollama: {e}"
