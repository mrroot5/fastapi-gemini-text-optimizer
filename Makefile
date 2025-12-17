.PHONY: publish deploy tests

ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

default: start

start:
	@poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

deploy:
	@gcloud run deploy --source .

tests:
	@poetry run pytest $(ARGS) -q

test:
	@poetry run pytest tests/test_gemini_service.py::test_transform_parses_valid_json -q


%:
	@:
