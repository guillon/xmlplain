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

TESTS=\
example-1.xml \
characters-mix-1.xml \
ctrl-endl-1.xml \
ctrl-endl-2.xml \
ctrl-m-1.xml \
ctrl-m-2.xml \
ctrl-tab-1.xml \
ctrl-below-32.xml \
dict-mix-1.xml \
empty-1.xml \
jenkins-sample-1.xml \
jenkins-sample-2.xml \
space-inner-1.xml \
special-mix.xml \
namespace-1.xml \
entity-1.xml \
entity-2.xml \
entity-3.xml \
unicode-1.xml \
unicode-2.xml

srcdir=$(abspath ..)
testdir=$(abspath .)
XMLPLAIN=$(srcdir)/xmlplain.py

COVERAGE=coverage
STRICT_COVERAGE=0
COVERAGE_HTML=1
PYTHON_COVERAGE_DIR=$(abspath $(testdir))/coverage
COVERAGE_ENV=env PYTHON_COVERAGE=1 STRICT_COVERAGE=$(STRICT_COVERAGE) COVERAGE_BIN=$(COVERAGE) PYTHONPATH=$(PYTHONPATH):$(abspath $(testdir))/coverage PYTHON_COVERAGE_DIR=$(PYTHON_COVERAGE_DIR) 

REF_XMLS=$(TESTS:%.xml=%.xml.ref)
REF_YMLS=$(TESTS:%.xml=%.yml.ref)
REF_PYMLS=$(TESTS:%.xml=%.p.yml.ref)
REF_PXMLS=$(TESTS:%.xml=%.p.xml.ref)
CHECK_EVTS=$(TESTS:%.xml=%.evt.chk)
CHECK_OBJS=$(TESTS:%.xml=%.obj.chk)
CHECK_YMLS=$(TESTS:%.xml=%.yml.chk)
CHECK_PYMLS=$(TESTS:%.xml=%.p.yml.chk)
CHECK_PXMLS=$(TESTS:%.xml=%.p.xml.chk)

all:

check: check-version check-doc check-evts check-objs check-ymls check-pymls check-pxmls check-non-test check-encoding

coverage:
	$(MAKE) coverage-start
	$(MAKE) coverage-check
	$(MAKE) coverage-stop

coverage-start:
	rm -rf $(PYTHON_COVERAGE_DIR)/.coverage* $(PYTHON_COVERAGE_DIR)/coverage.txt && mkdir -p $(PYTHON_COVERAGE_DIR)

coverage-check:
	$(MAKE) XMLPLAIN="env $(COVERAGE_ENV) $(XMLPLAIN)" check

coverage-stop:
	cd $(PYTHON_COVERAGE_DIR) && $(COVERAGE) combine
	[ "$(COVERAGE_HTML)" = "" ] || (cd $(PYTHON_COVERAGE_DIR) && env $(COVERAGE_ENV) ./report_coverage_html.sh)
	cd $(PYTHON_COVERAGE_DIR) && env $(COVERAGE_ENV) ./check_coverage.sh

clean: clean-coverage
	rm -f *.tmp *.out *.pyc

distclean: distclean-coverage
	rm -rf __pycache__

clean-coverage:
	rm -rf coverage/coverage.txt coverage/.coverage* coverage/html coverage/*.pyc

distclean-coverage: clean-coverage
	rm -rf coverage/__pycache__

check-version:
	$(XMLPLAIN) --version

check-doc:
	cd $(srcdir) && $(XMLPLAIN) --doctest

check-non-test:
	$(XMLPLAIN) example-1.xml example-1.xml.tmp
	$(XMLPLAIN) --filter evt example-1.xml example-1.xml.tmp
	$(XMLPLAIN) --outf py example-1.xml example-1.xml.tmp
	$(XMLPLAIN) --inf py example-1.xml.tmp example-1.xml.2.tmp
	$(XMLPLAIN) --outf py --filter evt example-1.xml example-1.xml.tmp
	$(XMLPLAIN) --inf py --filter evt example-1.xml.tmp example-1.xml.3.tmp

check-encoding:
	$(XMLPLAIN) --out-encoding iso-8859-1 unicode-1.xml unicode-1.xml.1.tmp
	$(XMLPLAIN) unicode-1.xml.1.tmp unicode-1.xml.2.tmp
	diff unicode-1.xml.ref unicode-1.xml.2.tmp
	$(XMLPLAIN) --out-encoding iso-8859-1 unicode-2.xml unicode-2.xml.1.tmp
	$(XMLPLAIN) --in-encoding iso-8859-1 unicode-2.xml.1.tmp unicode-2.xml.2.tmp
	diff unicode-2.xml.ref unicode-2.xml.2.tmp
	$(XMLPLAIN) --out-encoding iso-8859-1 --outf yml unicode-2.xml unicode-2.yml.1.tmp
	$(XMLPLAIN) --in-encoding iso-8859-1 --inf yml unicode-2.yml.1.tmp unicode-2.xml.3.tmp
	diff unicode-2.xml.ref unicode-2.xml.3.tmp

check-evts: $(CHECK_EVTS)

check-objs: $(CHECK_OBJS)

check-ymls: $(CHECK_YMLS)

check-pymls: $(CHECK_PYMLS)

check-pxmls: $(CHECK_PXMLS)

ref: ref-xmls ref-ymls ref-pymls ref-pxmls

ref-xmls: $(REF_XMLS)

ref-ymls: $(REF_YMLS)

ref-pymls: $(REF_PYMLS)

ref-pxmls: $(REF_PXMLS)


$(CHECK_EVTS): %.evt.chk: %.xml
	$(XMLPLAIN) --test --filter evt $*.xml $*.xml.evt.out
	diff $*.xml.ref $*.xml.evt.out
	$(XMLPLAIN) --test --in-process $$'\015' '&#xd;' --out-process '&#xd;' $$'\015' --string --filter evt $*.xml.evt.out $*.xml.evt.2.out
	diff $*.xml.ref $*.xml.evt.2.out

$(CHECK_OBJS): %.obj.chk: %.xml
	$(XMLPLAIN) --test --filter obj $*.xml $*.xml.obj.out
	diff $*.xml.ref $*.xml.obj.out
	$(XMLPLAIN) --test --in-process $$'\015' '&#xd;' --out-process '&#xd;' $$'\015' --string --filter obj $*.xml.obj.out $*.xml.obj.2.out
	diff $*.xml.ref $*.xml.obj.2.out

$(CHECK_YMLS): %.yml.chk: %.xml
	$(XMLPLAIN) --test --filter obj --outf yml $*.xml $*.yml.out
	diff $*.yml.ref $*.yml.out
	$(XMLPLAIN) --test --in-process $$'\015' '&#xd;' --out-process '&#xd;' $$'\015' --filter obj --inf yml --outf yml $*.yml.out $*.yml.2.out
	diff $*.yml.ref $*.yml.2.out

$(CHECK_PYMLS): %.p.yml.chk: %.xml
	$(XMLPLAIN) --test --pretty --filter obj --outf yml $*.xml $*.p.yml.out
	diff $*.p.yml.ref $*.p.yml.out
	$(XMLPLAIN) --test --bin --pretty --filter obj --outf yml $*.xml $*.p.yml.2.out
	diff $*.p.yml.ref $*.p.yml.2.out
	$(XMLPLAIN) --test --string --filter obj --inf yml --outf yml $*.p.yml.out $*.p.yml.3.out
	diff $*.p.yml.ref $*.p.yml.3.out
	$(XMLPLAIN) --test --string --bin --filter obj --inf yml --outf yml $*.p.yml.out $*.p.yml.4.out
	diff $*.p.yml.ref $*.p.yml.4.out

$(CHECK_PXMLS): %.p.xml.chk: %.xml
	$(XMLPLAIN) --test --pretty --filter obj $*.xml $*.p.xml.out
	diff $*.p.xml.ref $*.p.xml.out
	$(XMLPLAIN) --test --bin --pretty --filter obj $*.xml $*.p.xml.2.out
	diff $*.p.xml.ref $*.p.xml.2.out
	$(XMLPLAIN) --test --string --pretty --filter obj $*.p.xml.out $*.p.xml.3.out
	diff $*.p.xml.ref $*.p.xml.3.out
	$(XMLPLAIN) --test --string --bin --pretty --filter obj $*.p.xml.out $*.p.xml.4.out
	diff $*.p.xml.ref $*.p.xml.4.out

$(REF_XMLS): %.xml.ref: .FORCE
	$(XMLPLAIN) --test --filter evt $*.xml $*.xml.ref

$(REF_YMLS): %.yml.ref: .FORCE
	$(XMLPLAIN) --test --filter obj --outf yml $*.xml $*.yml.ref

$(REF_PYMLS): %.p.yml.ref: .FORCE
	$(XMLPLAIN) --test --pretty --filter obj --outf yml $*.xml $*.p.yml.ref

$(REF_PXMLS): %.p.xml.ref: .FORCE
	$(XMLPLAIN) --test --pretty --filter obj $*.xml $*.p.xml.ref

.FORCE:

.PHONY: all ref check clen distclean ref-evts ref-xmls ref-pxmls ref-ymls ref-pymls check-evts $(CHECK_EVTS) check-objs $(CHECK_OBJS) check-pxmls $(CHECK_PXMLS) check-ymls $(CHECK_YMLS) check-pymls $(CHECK_PYMLS) check-doc check-version check-non-test check-encoding coverage clean-coverage distclean-coverage coverage-start coverage-check coverage-stop
