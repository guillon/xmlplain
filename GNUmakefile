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

all: all-local all-tests

all-local:
	./setup.py build

all-tests:
	$(MAKE) -C tests all

check: check-local check-tests

check-local:

check-tests:
	$(MAKE) -C tests check

clean: clean-local clean-doc clean-tests

clean-local:
	rm -rf build xmlplain.pyc

clean-tests:
	$(MAKE) -C tests clean

distclean: distclean-local distclean-doc distclean-tests

distclean-local: clean
	rm -rf dist __pycache__ xmlplain.egg-info

distclean-tests:
	$(MAKE) -C tests distclean

install:
	./setup.py install --prefix=$(PREFIX)

dist:
	./setup.py sdist

doc:
	sphinx-build doc gh-pages

clean-doc:
	rm -rf gh-pages/.buildinfo gh-pages/.doctrees gh-pages/_modules gh-pages/_sources gh-pages/_static gh-pages/objects.inv gh-pages/*.html gh-pages/*.js

distclean-doc: clean-doc

.PHONY: all check clean distclean install dist doc all-local check-local clean-local distclean-local clean-doc distclean-doc all-tests check-tests clean-tests disclean-tests
