FILES = $(shell git ls-files)

all: mypy pylint

pylint:
	pylint --disable=duplicate-code *.py

mypy:
	mypy *.py

ARCH.tar.gz:$(FILES)
	ln -s . ARCH ; tar -cvf - $(FILES) | gzip -9 >$@ ; rm ARCH
