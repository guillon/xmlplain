#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
#

PREFIX=/usr/local

XMLPLAIN=$(abspath xmlplain.py)
COVERAGE=python-coverage

REPO=https://github.com/guillon/xmlplain

all: all-local all-tests

all-local:
	./setup.py build

all-tests:
	$(MAKE) -C tests XMLPLAIN="$(XMLPLAIN)" all

check: check-local check-tests

check-local: all-local

check-tests:
	$(MAKE) -C tests XMLPLAIN="$(XMLPLAIN)" check

coverage:
	$(MAKE) -C tests XMLPLAIN="$(XMLPLAIN)" COVERAGE="$(COVERAGE)" coverage

clean: clean-local clean-doc clean-tests

clean-local:
	rm -rf build xmlplain.pyc

clean-tests:
	$(MAKE) -C tests clean

distclean: distclean-local distclean-doc distclean-tests

distclean-local: clean
	rm -rf dist __pycache__ xmlplain.egg-info venv2 venv3

distclean-tests:
	$(MAKE) -C tests distclean

install:
	./setup.py install --prefix=$(PREFIX)

sdist:
	./setup.py sdist

bdist:
	./setup.py bdist_wheel

doc:
	sphinx-build doc html

upload:
	twine upload dist/xmlplain-*.tar.gz dist/xmlplain-*.whl

upload-doc:
	rm -rf gh-pages
	(mkdir gh-pages && cd gh-pages && git init && \
	git fetch "$(REPO)" refs/heads/gh-pages && git checkout FETCH_HEAD)
	rm -rf gh-pages/* && cp -a html/* gh-pages/
	(cd gh-pages && git add -A)
	(cd gh-pages && git commit -m 'Update doc' || true)
	(cd gh-pages &&	git push "$(REPO)" HEAD:refs/heads/gh-pages)

requirements:
	pip install -r requirements.txt
	pip install coverage

upload-requirements:
	pip install twine

doc-requirements:
	pip install sphinx

self-requirements:
	pip install --upgrade xmlplain

release-coverage-venv23:
	$(MAKE) -C tests coverage-start
	env VIRTUAL_ENV="$$PWD/venv2/bin" \
	PATH="$$PWD/venv2/bin:$$PATH" \
	$(MAKE) -C tests coverage-check
	env VIRTUAL_ENV="$$PWD/venv3/bin" \
	PATH="$$PWD/venv3/bin:$$PATH" \
	$(MAKE) -C tests coverage-check
	env VIRTUAL_ENV="$$PWD/venv3/bin" \
	PATH="$$PWD/venv3/bin:$$PATH" \
	$(MAKE) -C tests STRICT_COVERAGE=1 coverage-stop

release:
	$(MAKE) distclean
	$(MAKE) venv2 venv3
	$(MAKE) venv2-requirements venv3-requirements
	$(MAKE) release-coverage-venv23
	$(MAKE) release-venv2 release-venv3

release-venv2 release-venv3: release-%:
	$(MAKE) $*-requirements
	$(MAKE) $*-bdist
	[ "$*" != "venv3" ] || $(MAKE) venv3-sdist
	[ "$*" != "venv3" ] || $(MAKE) venv3-doc-requirements
	[ "$*" != "venv3" ] || $(MAKE) venv3-doc

release-upload:
	$(MAKE) release-upload-doc
	$(MAKE) release-upload-pypi

release-upload-pypi:
	$(MAKE) venv3-upload-requirements
	$(MAKE) venv3-upload

release-upload-doc:
	$(MAKE) upload-doc

release-check:
	$(MAKE) distclean
	$(MAKE) venv2 venv3
	$(MAKE) release-check-venv2 release-check-venv3

release-check-venv2 release-check-venv3: release-check-%:
	$(MAKE) $*-self-requirements
	$(MAKE) XMLPLAIN="python -m xmlplain" $*-check

venv2-%:
	env VIRTUAL_ENV="$$PWD/venv2/bin" \
	PATH="$$PWD/venv2/bin:$$PATH" \
	$(MAKE) $*

venv3-%:
	env VIRTUAL_ENV="$$PWD/venv3/bin" \
	PATH="$$PWD/venv3/bin:$$PATH" \
	$(MAKE) $*

venv2:
	virtualenv -p python2 venv2
	venv2/bin/pip install --upgrade pip setuptools wheel

venv3:
	virtualenv -p python3 venv3
	venv3/bin/pip install --upgrade pip setuptools wheel certifi
	[ ! -f /etc/ssl/certs/ca-certificates.crt ] || cp /etc/ssl/certs/ca-certificates.crt venv3/lib/python3*/site-packages/certifi/cacert.pem

clean-doc:
	rm -rf html gh-pages

distclean-doc: clean-doc

.PHONY: all check clean distclean install sdist bdist doc upload
.PHONY: all-local check-local clean-local distclean-local
.PHONY: doc clean-doc distclean-doc
.PHONY: all-tests check-tests clean-tests disclean-tests
.PHONY: release release-venv2 release-venv3 release-upload release-upload-pypi release-upload-doc release-check release-check-venv2 release-check-venv3 requirements upload-requirements doc-requirements self-requirements
.PHONY: venv2-% venv3-%
.PHONY: coverage release-coverage-venv23
