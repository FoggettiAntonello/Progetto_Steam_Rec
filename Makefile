PYTHON=python

run:
	$(PYTHON) -m src.main

refresh:
	$(PYTHON) -m src.main --refresh

ask:
	$(PYTHON) -m src.main --query "$(q)"

category:
	$(PYTHON) -m src.main --refresh --category "$(c)"

clean:
	if exist chroma_db (rmdir /s /q chroma_db)
