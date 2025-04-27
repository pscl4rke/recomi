
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
release: pyversion != python3 setup.py --version
release: gitversion != git describe --tags
release:
	@echo 'Py version:  $(pyversion)'
	@echo 'Git version: $(gitversion)'
	test '$(pyversion)' = '$(gitversion)'
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv *egg-info -i dist
	mv dist dist.$$(date +%Y%m%d.%H%M%S)
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

docker-to-run += test-in-docker-3.7-slim-bullseye
docker-to-run += test-in-docker-3.8-slim-bullseye
docker-to-run += test-in-docker-3.9-slim-bullseye
docker-to-run += test-in-docker-3.10-slim-bullseye
docker-to-run += test-in-docker-3.11-slim-bullseye
docker-to-run += test-in-docker-3.12-slim-bookworm
docker-to-run += test-in-docker-3.13-slim-bookworm
test-in-docker: $(docker-to-run)

test-in-docker-%:
	@echo
	@echo "===================================================="
	@echo "Testing with docker.io/library/python:$*"
	@echo "===================================================="
	@echo
	ephemerun \
		-i "docker.io/library/python:$*" \
		-v ".:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install .[dev]" \
		-S "coverage run -m unittest discover test/" \
		-S "coverage report -m"
