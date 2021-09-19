
.PHONY: test
test:
	python3 -m unittest discover test

dev:
	mkdir dev
	ln -s ../recomi ../setup.cfg ../setup.py dev/.
	python3 -m venv dev/venv
	./dev/venv/bin/pip install --editable ./dev
