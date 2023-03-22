FOLDER_PROJECT = mancala_backend/
TESTS_FOLDER = tests/

.PHONY: tests
tests: ## Run all unit tests.
	@poetry run python -m unittest -v -s tests/

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
