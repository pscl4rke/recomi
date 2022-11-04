
.PHONY: test
test:
	python3 -m unittest discover test

dev:
	mkdir dev
	ln -s ../recomi ../setup.cfg ../setup.py dev/.
	python3 -m venv dev/venv
	./dev/venv/bin/pip install --editable ./dev

export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release:
	test ! -d dist
	python3 setup.py sdist
	twine upload dist/*
	mv *egg-info -i dist
	mv dist dist.$$(date +%Y%m%d.%H%M%S)
	@echo
	@echo
	@echo REMEMBER TO REBUILD AND REDEPLOY recomi.debian TOO
	@echo
	@echo
