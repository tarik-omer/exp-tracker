build:
	export FLASK_APP=app:app
	export FLASK_DEBUG=1

run:
	flask run

install:
	pip install -r requirements.txt
