.PHONY: publish deploy

default: start

start:
	@poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

deploy:
	@gcloud run deploy --source .
