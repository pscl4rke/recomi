
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
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
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

####

docker-to-run += test-in-docker-3.7-slim-bullseye
test-in-docker: $(docker-to-run)

test-in-docker-%:
	@echo
	@echo "===================================================="
	@echo "Testing with python:$*"
	@echo "===================================================="
	@echo
	ephemerun \
		-i "python:$*" \
		-v ".:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install .[dev]" \
		-S "coverage run -m unittest discover test/" \
		-S "coverage report -m"
