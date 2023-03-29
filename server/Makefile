FOLDER_PROJECT = mancala_backend/
TESTS_FOLDER = tests/

start: ## Starts the backend server.
	@poetry run python ${FOLDER_PROJECT}/main.py

.PHONY: tests
tests: ## Run all unit tests.
	@poetry run python -m unittest discover -v -b --locals -s $(TESTS_FOLDER) 

black: ## Run black inside the project folder.
	@poetry run black $(FOLDER_PROJECT)

isort: ## Run isort inside the project and the tests folder.
	@poetry run isort $(FOLDER_PROJECT)
	@poetry run isort $(TESTS_FOLDER)

bandit: ## Run bandit inside the project folder.
	@poetry run bandit -r $(FOLDER_PROJECT)

code_review: ## Run complete code review policy.
	@$(MAKE) isort
	@$(MAKE) black
	@$(MAKE) bandit
