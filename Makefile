VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) src/main.py

parse: $(VENV)/bin/activate
	$(PYTHON) src/parser.py

bind: $(VENV)/bin/activate
	gunicorn --bind 0.0.0.0:5000 src/wsgi:app

 #$(VENV)/bin/activate: requirements.txt
setup: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
