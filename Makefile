SHELL := /bin/bash
lint:
	source bin/activate && flake8 djenga
	source bin/activate && pylint --rcfile djenga.pylintrc djenga

test:
	source bin/activate \
	  && pytest --cov=djenga tests/

