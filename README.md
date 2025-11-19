# 🎮 Steam Game Recommender (RAG System)

Un sistema di **RAG (Retrieval Augmented Generation)** che utilizza:

- **Ollama + LLaMA 3** per la generazione delle risposte  
- **SteamSpy API** per ottenere dati reali sui videogiochi  
- **ChromaDB** come database vettoriale  
- **Sentence-Transformers** per generare embeddings  
- Interfaccia CLI migliorata con **Rich**

Il sistema permette di chiedere:

> *"Quali sono i migliori roguelike?"*  
> *"Mostrami giochi di calcio popolari"*  
> *"Dammi RPG con alto numero di giocatori attivi"*

E fornisce liste ordinate, precise e filtrate per genere.

---

# 🚀 Funzionalità principali

✔ Database completo di giochi presi da SteamSpy  
✔ Recupero intelligente basato su embeddings  
✔ Filtraggio severo dei generi (no più “bowling roguelike”)  
✔ Risposte in italiano o inglese automaticamente  
✔ Output formattato in Markdown  
✔ Pronto per evolvere in una Web App o GUI  

---

# 📦 Requisiti

- Python **3.10+**
- Ollama installato:  
  https://ollama.com
- Modello LLaMA 3 scaricato:
```bash
ollama pull llama3
