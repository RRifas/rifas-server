# ===========
# = Run app =
# ===========

start: ## Run app
	hypercorn --reload apirifas.py

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
