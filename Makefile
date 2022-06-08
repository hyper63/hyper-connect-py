## Lint your code using pylint
.PHONY: lint
lint:
	bash .git/hooks/pre-commit
.PHONY: test
test:
	python -m unittest discover -s tests -v
.PHONY: black
black:
	python -m black --version
	python -m black .## Run ci part
.PHONY: ci
    ci: lint test
toc:
	cat README.md | bash toc.sh 2 2
