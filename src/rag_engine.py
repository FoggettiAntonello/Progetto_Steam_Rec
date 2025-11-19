import ollama
from typing import List
from src.config import Config


class RAGEngine:
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.language = Config.DEFAULT_LANGUAGE

        self.base_prompt = """
You are a deterministic Steam game database assistant.
You must follow these strict rules:

1. LANGUAGE:
   Respond strictly in: {LANG}. Never mix languages.

2. FILTERING:
   Only output games whose "Genre/Genere" matches the category requested.
   Never invent titles. Only use items present in CONTEXT DATA.

3. NO MATCHES:
   If and only if CONTEXT DATA is completely empty, output exactly:
   "Nessun gioco trovato per questa categoria specifica".

4. IF CONTEXT EXISTS:
   - NEVER include the sentence "Nessun gioco trovato per questa categoria specifica".
   - NEVER add notes, warnings, or fallback messages.
   - NEVER explain that some games may not fully match.
   - Simply return EXACTLY 5 valid games from the provided CONTEXT DATA.

5. FORMAT:
   Provide EXACTLY 5 bullet points.
   Format each as:
   **NAME** – CCU – short description.

6. OUTPUT:
   Your final answer MUST be clean, structured, and in Markdown.
"""

    def set_language(self, lang: str):
        self.language = lang

    def generate_answer(self, query: str, context_chunks: List[str]) -> str:
        has_context = len(context_chunks) > 0

        prompt = self.base_prompt.replace("{LANG}", self.language)

        if has_context:
            prompt += "\nCONTEXT IS NOT EMPTY: YOU MUST RETURN GAMES.\n"

        context = "\n\n".join(context_chunks)

        user_prompt = (
            f"{prompt}\n\n"
            f"### 📘 CONTEXT DATA\n{context}\n\n"
            f"### ❓ USER QUESTION\n{query}\n\n"
            f"### 🧠 TASK\n"
            f"Produce una risposta pulita, formattata, senza note, commenti o avvisi aggiuntivi."
        )

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={"temperature": self.temperature},
            )

            return response["message"]["content"].strip()

        except Exception as e:
            return f"⚠️ Errore Ollama: {e}"
