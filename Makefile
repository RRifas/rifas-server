# ===========
# = Run app =
# ===========

start: ## Run app
	uvicorn main:app --reload --port 8000

start-prod: ## Run app
	uvicorn main:app --port ${PORT}

# ==================
# = Pip management =
# ==================

requirements: #update requirements file
	pip freeze > requirements.txt

pip-install: ## Install pip requirements
	pip install -r ./requirements.txt

# =========
# = Tests =
# =========

test: ## Run tests
	pytest ./tests
