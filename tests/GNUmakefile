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
unicode-1.xml

TOP=$(abspath ..)
XMLPLAIN=$(TOP)/xmlplain.py)

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

check: check-doc check-evts check-objs check-ymls check-pymls check-pxmls

clean:
	rm -f *.tmp *.out

distclean: clean

check-doc:
	cd $(TOP) && $(XMLPLAIN) --doctest

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
	$(XMLPLAIN) --test --filter evt $*.xml.evt.out $*.xml.evt.2.out
	diff $*.xml.ref $*.xml.evt.2.out

$(CHECK_OBJS): %.obj.chk: %.xml
	$(XMLPLAIN) --test --filter obj $*.xml $*.xml.obj.out
	diff $*.xml.ref $*.xml.obj.out
	$(XMLPLAIN) --test --filter obj $*.xml.obj.out $*.xml.obj.2.out
	diff $*.xml.ref $*.xml.obj.2.out

$(CHECK_YMLS): %.yml.chk: %.xml
	$(XMLPLAIN) --test --filter obj --outf yml $*.xml $*.yml.out
	diff $*.yml.ref $*.yml.out

$(CHECK_PYMLS): %.p.yml.chk: %.xml
	$(XMLPLAIN) --test --pretty --filter obj --outf yml $*.xml $*.p.yml.out
	diff $*.p.yml.ref $*.p.yml.out
	$(XMLPLAIN) --test --filter obj --inf yml --outf yml $*.p.yml.out $*.p.yml.2.out
	diff $*.p.yml.ref $*.p.yml.2.out

$(CHECK_PXMLS): %.p.xml.chk: %.xml
	$(XMLPLAIN) --test --pretty --filter obj $*.xml $*.p.xml.out
	diff $*.p.xml.ref $*.p.xml.out
	$(XMLPLAIN) --test --pretty --filter obj $*.p.xml.out $*.p.xml.2.out
	diff $*.p.xml.ref $*.p.xml.2.out

$(REF_XMLS): %.xml.ref: .FORCE
	$(XMLPLAIN) --test --filter evt $*.xml $*.xml.ref

$(REF_YMLS): %.yml.ref: .FORCE
	$(XMLPLAIN) --test --filter obj --outf yml $*.xml $*.yml.ref

$(REF_PYMLS): %.p.yml.ref: .FORCE
	$(XMLPLAIN) --test --pretty --filter obj --outf yml $*.xml $*.p.yml.ref

$(REF_PXMLS): %.p.xml.ref: .FORCE
	$(XMLPLAIN) --test --pretty --filter obj $*.xml $*.p.xml.ref

.FORCE:

.PHONY: all ref check clen distclean ref-evts ref-xmls ref-pxmls ref-ymls ref-pymls check-evts $(CHECK_EVTS) check-objs $(CHECK_OBJS) check-pxmls $(CHECK_PXMLS) check-ymls $(CHECK_YMLS) check-pymls $(CHECK_PYMLS)
