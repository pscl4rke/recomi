
# FIXME: calls to setup.py directly are now deprected, so I need to fix the --version usage
#	https://packaging.python.org/en/latest/guides/modernize-setup-py-project/

# These add a delay to every make invocation (inc tab completion)
#pyversion != python3 setup.py --version
#gitversion != git describe --tags

testdir := test

.PHONY: test
test: | dev
	cd dev && ./venv/bin/coverage run -m unittest discover $(testdir)
	cd dev && ./venv/bin/coverage report -m

dev:
	mkdir dev
	ln -s ../recomi ../test ../setup.cfg ../setup.py dev/.

dev/venv: setup.cfg | dev
	python3 -m venv dev/venv
	./dev/venv/bin/pip install --editable ./dev[dev]
	touch $@

pre-release-checks: dev/venv
	./dev/venv/bin/pyroma . || true

####

tagged-commit: version != python3 setup.py --version
tagged-commit:
	git diff | grep '^+__version__'
	git add .
	git commit -m "Release $(version)"
	git tag -a -m "Release $(version)" "$(version)"
	@echo
	@echo "Now do a release, and then remember to push!"

release: export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release: pre-release-checks
	test '$(shell python3 setup.py --version)' = '$(shell git describe)'
	test ! -d dist
	pyproject-build
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv -i *.egg-info dist/.
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)
	@echo
	@echo
	@echo REMEMBER TO PUSH ANY NEW GIT TAGS
	@echo
	@echo REMEMBER TO REBUILD AND REDEPLOY recomi.debian TOO
	@echo
	@echo

####

image-to-run += test-in-container-3.7-slim-bullseye
image-to-run += test-in-container-3.8-slim-bullseye
image-to-run += test-in-container-3.9-slim-bullseye
image-to-run += test-in-container-3.10-slim-bullseye
image-to-run += test-in-container-3.11-slim-bullseye
image-to-run += test-in-container-3.12-slim-bookworm
image-to-run += test-in-container-3.13-slim-bookworm
image-to-run += test-in-container-3.14-slim-trixie

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
		-v "`pwd`:/root/src:ro" \
		-W "/root" \
		-S "cp -air ./src/* ." \
		-S "pip --no-cache-dir install .[dev]" \
		-S "coverage run -m unittest discover $(testdir)" \
		-S "coverage report -m" \
		-S "(pyroma . || true)"
