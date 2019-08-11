SHELL := /bin/bash
lint:
	source bin/activate && flake8 djenga
	source bin/activate && pylint --rcfile djenga.pylintrc djenga

test:
	source bin/activate \
	  && coverage run --source='djenga' \
	      manage.py test -k -v2 --debug-mode
	source bin/activate \
	  && coverage report --show-missing --include='$*/*'
