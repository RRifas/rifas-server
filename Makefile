# ===========
# = Run app =
# ===========

start: ## Run app
	uvicorn apirifas:app --reload --port 8000

start-prod: ## Run app
	uvicorn apirifas:app --port ${PORT}

# ==================
# = Pip management =
# ==================

pip-install: ## Install pip requirements
	pip install -r ./requirements.txt

# =========
# = Tests =
# =========

test: ## Run tests
	pytest ./tests
