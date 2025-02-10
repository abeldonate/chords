VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) src/main.py

parse: $(VENV)/bin/activate
	$(PYTHON) src/parse_song.py

setup: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
