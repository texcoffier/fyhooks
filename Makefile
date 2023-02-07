all: mypy pylint

pylint:
	pylint --disable=duplicate-code *.py

mypy:
	mypy *.py

