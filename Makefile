
# These add a delay to every make invocation (inc tab completion)
#pyversion != python3 setup.py --version
#gitversion != git describe --tags

.PHONY: test
test: | dev
	cd dev && ./venv/bin/coverage run -m unittest discover ./test
	cd dev && ./venv/bin/coverage report -m

dev:
	mkdir dev
	ln -s ../recomi ../test ../setup.cfg ../setup.py dev/.
	python3 -m venv dev/venv
	./dev/venv/bin/pip install --editable ./dev[dev]

release: export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release:
	test '$(shell python3 setup.py --version)' = '$(shell git describe --tags)'
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv *egg-info -i dist
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)
	@echo
	@echo
	@echo REMEMBER TO PUSH ANY NEW GIT TAGS
	@echo
	@echo REMEMBER TO REBUILD AND REDEPLOY recomi.debian TOO
	@echo
	@echo

pre-release-checks:
	pyroma .

####

image-to-run += test-in-container-3.7-slim-bullseye
image-to-run += test-in-container-3.8-slim-bullseye
image-to-run += test-in-container-3.9-slim-bullseye
image-to-run += test-in-container-3.10-slim-bullseye
image-to-run += test-in-container-3.11-slim-bullseye
image-to-run += test-in-container-3.12-slim-bookworm
image-to-run += test-in-container-3.13-slim-bookworm

test-in-container: $(image-to-run)
	@echo
	@echo "=============================================================="
	@echo "Successfully tested all versions with ephemerun:"
	@echo "$^" | tr ' ' '\n'
	@echo "=============================================================="
	@echo

test-in-container-%:
	@echo
	@echo "=============================================================="
	@echo "Testing with docker.io/library/python:$*"
	@echo "=============================================================="
	@echo
	ephemerun \
		-i "docker.io/library/python:$*" \
		-v ".:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install .[dev]" \
		-S "coverage run -m unittest discover test/" \
		-S "coverage report -m"
