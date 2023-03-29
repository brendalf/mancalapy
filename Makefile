game/start: ## Starts the game servers
	@docker compose build
	@docker compose up -d

game/logs: ## Open logas
	@docker compose logs -f

game/stop: ## Stop game servers
	@docker compose down
