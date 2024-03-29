
.PHONY: test
test: | dev
	cd dev && ./venv/bin/coverage run -m unittest discover ./test
	cd dev && ./venv/bin/coverage report -m

dev:
	mkdir dev
	ln -s ../recomi ../test ../setup.cfg ../setup.py dev/.
	python3 -m venv dev/venv
	./dev/venv/bin/pip install --editable ./dev[dev]

export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release:
	test ! -d dist
	python3 setup.py sdist
	twine check dist/*
	twine upload dist/*
	mv *egg-info -i dist
	mv dist dist.$$(date +%Y%m%d.%H%M%S)
	@echo
	@echo
	@echo REMEMBER TO REBUILD AND REDEPLOY recomi.debian TOO
	@echo
	@echo

pre-release-checks:
	pyroma .
