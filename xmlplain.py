#!/usr/bin/env python
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

"""
XML as plain object module.

This module is a set of utility functions for parsing XML input
into plain list/dict/string types.

These plain XML objects in turn can be emitted through YAML
for instance as bare YAML without python objects.

The motivating usage is to dump XML to YAML, manually edit
files as YAML, and emit XML output back.

The original XML file is supposed to be preserved except
for comments and if requested spaces between elements.

Note that there are alternative modules with nearly the same
functionality, but none of them both provide simple plain objects
and preserve the initial XML content even for non structured XML.

WARNING: the implementation does not support XML namespaces
and entity location. If this is found useful, please add an issue.

:Example:
    >>> import xmlplain, sys

    >>> _ = sys.stdout.write(open("tests/example-1.xml").read())
    <example>
      <doc>This is an example for xmlobj documentation. </doc>
      <content version="beta">
        <kind>document</kind>
        <class>example</class>
        <structured/>
        <elements>
          <item>Elt 1</item>
          <doc>Elt 2</doc>
          <item>Elt 3</item>
          <doc>Elt 4</doc>
        </elements>
      </content>
    </example>

    >>> root = xmlplain.xml_to_obj(open("tests/example-1.xml"), strip_space=True, fold_dict=True)
    >>> xmlplain.obj_to_yaml(root, sys.stdout)
    example:
      doc: 'This is an example for xmlobj documentation. '
      content:
        '@version': beta
        kind: document
        class: example
        structured: ''
        elements:
        - item: Elt 1
        - doc: Elt 2
        - item: Elt 3
        - doc: Elt 4

    >>> xmlplain.xml_from_obj(root, sys.stdout)
    <?xml version="1.0" encoding="UTF-8"?>
    <example>
      <doc>This is an example for xmlobj documentation. </doc>
      <content version="beta">
        <kind>document</kind>
        <class>example</class>
        <structured></structured>
        <elements>
          <item>Elt 1</item>
          <doc>Elt 2</doc>
          <item>Elt 3</item>
          <doc>Elt 4</doc>
        </elements>
      </content>
    </example>


"""

from __future__ import print_function

__version__ = '1.0.2'

import yaml, sys, xml, io
from xml.sax.saxutils import XMLGenerator
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def xml_to_events(inf, evt_receiver=None, quoting=None):
    """
    Generates XML events tuples from the input stream.

    The generated events consist of pairs: (type, value)
    where type is a single char identifier for the event and
    value is a variable length tuple.
    Events correspond to xml.sax events with the exception that
    attributes are generated as events instead of being part of
    the start element event.

    :param inf: the input stream (passed to xml.sax.parse())
    :param evt_receiver: a receiver implementing the append() method or None,
      in which case a new list will be generated
    :param quoting: a mapping str -> str for quoting input content or None,
      the default is: {"\\r: ""} (i.e. remove all "\\r" from the input)

    :return: returns the evt_receiver or the generated list

    Events are:
    - ("[", ("",)) for the document start
    - ("]", ("",)) for the document end
    - ("<", (elt_name,)) for an element start
    - (">", (elt_name,)) for an element end
    - ("@", (attr_name, attr_value)) for an attribute associated to the
    last start element
    - ("|", (content,)) for a CDATA string content
    - ("#", (whitespace,)) for an ignorable whitespace string

    .. warning: namespace events and location events available in xml.sax are
      ignored from the input stream
    .. seealso: xml_from_events(), xml.sax.parse()
    """
    class EventGenerator(xml.sax.ContentHandler):
        def __init__(self, evt_receiver, quoting=None):
            self.evt_receiver = evt_receiver
            # by default remove '\r' early as it is
            # ends up being removed by editors anyway
            self.quoting = {'\r': ''} if quoting == None else quoting

        def quote(self, content):
            if self.quoting:
                for k, v in self.quoting.items():
                    content = content.replace(k, v)
            return content
        def startElement(self, name, attrs):
            self.evt_receiver.append(("<", (name,)))
            # Enforce a stable order as sax attributes are unordered
            for attr in sorted(attrs.keys()):
                evt_receiver.append(("@", (attr, attrs[attr])))
        def endElement(self, name):
            self.evt_receiver.append((">", (name,)))
        def startDocument(self):
            self.evt_receiver.append(("[", ("",)))
        def endDocument(self):
            self.evt_receiver.append(("]", ("",)))
        def characters(self, content):
            self.evt_receiver.append(("|", (self.quote(content),)))
        def ignorableWhiteSpace(self, whitespace):
            self.evt_receiver.append(("#", (whitespace,)))
    if evt_receiver == None: evt_receiver = []
    xml.sax.parse(inf, EventGenerator(evt_receiver, quoting=quoting))
    return evt_receiver


def xml_from_events(evts, outf=sys.stdout, encoding='UTF-8', quoting=None):
    """
    Outputs the XML document from the events tuples.

    From the given events tuples lists as specified in xml_to_events(),
    generated a well formed XML document.

    :param evts: events tuples list or iterator
    :param outf: output file stream passed to xml.saxutils.XMLGenerator()
    :param encoding: output encoding passed to xml.saxutils.XMLGenerator()
    :param quoting: a mapping str -> str for quoting output content or None,
      the default is the map: {} (i.e. no quoting)

    .. note: unknown events types are ignored
    .. seealso: xml_to_events(), xml.sax.saxutils.XMLGenerator()
    """
    class SaxGenerator():
        def __init__(self, sax_receiver, quoting=None):
            self.sax_receiver = sax_receiver
            self.allowed = ["["]
            self.quoting = {} if quoting == None else quoting
        def unquote(self, content):
            if self.quoting:
                for k, v in self.quoting.items():
                    content = content.replace(v, k)
            return content
        def append(self, evt):
            kind, value = evt
            if kind == '[':
                self.sax_receiver.startDocument()
                self.start = None
                return
            if kind == '@':
                self.start[1][value[0]] = value[1]
                return
            if self.start != None:
                self.sax_receiver.startElement(*self.start)
                self.start = None
            if kind == ']':
                self.sax_receiver.endDocument()
            elif kind == '<':
                self.start = (value[0], OrderedDict())
            elif kind == '>':
                self.sax_receiver.endElement(value[0])
            elif kind == '|':
                self.sax_receiver.characters(self.unquote(value[0]))
            elif kind == '#':
                self.sax_receiver.ignorableWhitespace(value[0])
    generator = XMLGenerator(outf, encoding=encoding)
    generator = SaxGenerator(generator, quoting=quoting)
    for evt in evts: generator.append(evt)


def xml_to_obj(inf, strip_space=False, fold_dict=False):
    """
    Generate an plain object representation from the XML input.

    The representation consists of lists of plain
    elements which are either XML elements as dict
    { elt_name: children_list } or XML CDATA text contents as
    plain strings.
    This plain object for a XML document can be emitted to
    YAML for instance with no python dependency.

    When the 'fold' option is given, an elements list may be
    simplified into a multiple key ordered dict or a single text content.
    Note that in this case, some Ordered dict python objects may be generated,
    one should then use the obj_to_yaml() method in order to get a bare
    YAML output.

    When the 'strip_space' option is given, non-leaf text content
    are striped, this is in most case safe when managing structured
    XML, though, note that this change your XML document content.
    Generally one would use this in conjonction with pretty=true
    when emitting back the object to XML with xml_from_obj().

    :param inf: the input XML file stream
    :param strip_space: strip spaces from non-leaf text content
    :param fold_dict: optimized unambiguous lists of dict into ordered dicts

    :return: the root of the generated plain object, actually a single key dict

    :Example:

    >>> import xmlplain, yaml, sys
    >>> root = xmlplain.xml_to_obj(open("tests/example-1.xml"), strip_space=True)
    >>> yaml.dump(root, sys.stdout, default_flow_style=False)
    example:
    - doc: 'This is an example for xmlobj documentation. '
    - content:
      - '@version': beta
      - kind: document
      - class: example
      - structured: ''
      - elements:
        - item: Elt 1
        - doc: Elt 2
        - item: Elt 3
        - doc: Elt 4

    >>> root = xmlplain.xml_to_obj(open("tests/example-1.xml"), strip_space=True, fold_dict=True)
    >>> xmlplain.obj_to_yaml(root, sys.stdout)
    example:
      doc: 'This is an example for xmlobj documentation. '
      content:
        '@version': beta
        kind: document
        class: example
        structured: ''
        elements:
        - item: Elt 1
        - doc: Elt 2
        - item: Elt 3
        - doc: Elt 4

    .. seealso: xml_from_obj()
    """
    class ObjGenerator():
        def __init__(self, strip_space=False, fold_dict=False):
            self.value = None
            self.strip_space = strip_space
            self.fold_dict = fold_dict
        def get_value(self):
            return self.value
        def strip_space_elts(self, elts):
            # Only strip space when not a leaf
            if len(elts) <= 1: return elts
            elts = [e for e in
                    [s.strip() if not isinstance(s, dict) else s for s in elts]
                    if e != ""]
            return elts
        def fold_dict_elts(self, elts):
            if len(elts) <= 1: return elts
            # Simplify into an OrderedDict if there is no mixed text and no key duplicates
            keys = ['#' if not isinstance(e, dict) else list(e.keys())[0] for e in elts]
            unique_keys = list(set(keys))
            if len(unique_keys) == len(keys) and '#' not in unique_keys:
                return OrderedDict([list(elt.items())[0] for elt in elts])
            return elts
        def fold_trivial(self, elts):
            if isinstance(elts, list):
                if len(elts) == 0: return ""
                if len(elts) == 1: return elts[0]
            return elts
        def process_children(self):
            name, children = list(self.stack[-1].items())[0]
            children = self.children()
            if self.strip_space: children = self.strip_space_elts(children)
            if self.fold_dict: children = self.fold_dict_elts(children)
            children = self.fold_trivial(children)
            self.stack[-1][name] = children
        def children(self):
            return list(self.stack[-1].values())[0]
        def push_elt(self, name):
            elt = {name: []}
            self.children().append(elt)
            self.stack.append(elt)
        def pop_elt(self, name):
            self.stack.pop()
        def append_attr(self, name, value):
            self.children().append({'@%s' % name: value})
        def append_content(self, content):
            children = self.children()
            if len(children) > 0 and not isinstance(children[-1], dict):
                children[-1] += content
            else:
                children.append(content)
        def append(self, event):
            kind, value = event
            if kind == '[':
                self.stack = [{'_': []}]
            elif kind == ']':
                self.value = self.children()[0]
            elif kind == '<':
                self.push_elt(value[0])
            elif kind == '>':
                self.process_children()
                self.pop_elt(value[0])
            elif kind == '@':
                self.append_attr(value[0], value[1])
            elif kind == '|':
                self.append_content(value[0])
            elif kind == '#':
                pass
    return xml_to_events(inf, ObjGenerator(strip_space=strip_space, fold_dict=fold_dict)).get_value()


def events_filter_pretty(events, evt_receiver=None, indent="  "):
    """
    Augment an XML event list for pretty printing.

    This is a filter function taking an event stream and returning the
    augmented event stream including ignorable whitespaces for an indented
    pretty print. the generated events stream is still a valid events stream
    suitable for xml_from_events().

    :param events: the input XML events stream
    :param evt_receiver: the new events receiver or None for newly generated list
    :param indent: the base indent string, defaults to 2-space indent

    :return: the evt_receiver if not None or the newly created events list

    .. seealso: xml_from_event()
    """
    class EventFilterPretty():
        def __init__(self, evt_receiver, indent="  "):
            self.evt_receiver = evt_receiver
            self.indent = indent
        def filter(self, evts):
            evts = iter(evts)
            lookahead = []
            depth = 0
            while True:
                if len(lookahead) == 0:
                    while True:
                        e = next(evts, None)
                        if e == None: break
                        lookahead.append(e)
                        if e[0] in [">", "]"]: break
                    if len(lookahead) == 0: break
                kinds = list(next(iter(zip(*lookahead))))
                if kinds[0] == "<" and not "<" in kinds[1:]:
                    if depth > 0: self.evt_receiver.append(('#', ('\n',)))
                    self.evt_receiver.append(('#', (self.indent * depth,)))
                    while lookahead[0][0] != ">": self.evt_receiver.append(lookahead.pop(0))
                    self.evt_receiver.append(lookahead.pop(0))
                    if depth == 0: self.evt_receiver.append(('#', ('\n',)))
                else:
                    if kinds[0] == "<":
                        if depth > 0: self.evt_receiver.append(('#', ('\n',)))
                        self.evt_receiver.append(('#', (self.indent * depth,)))
                        self.evt_receiver.append(lookahead.pop(0))
                        depth += 1
                    elif kinds[0] == ">":
                        depth -= 1
                        self.evt_receiver.append(('#', ('\n',)))
                        self.evt_receiver.append(('#', (self.indent * depth,)))
                        self.evt_receiver.append(lookahead.pop(0))
                        if depth == 0: self.evt_receiver.append(('#', ('\n',)))
                    elif kinds[0] == "|":
                        self.evt_receiver.append(('#', ('\n',)))
                        self.evt_receiver.append(('#', (self.indent * depth,)))
                        self.evt_receiver.append(lookahead.pop(0))
                    else:
                        self.evt_receiver.append(lookahead.pop(0))
            assert(next(evts, None) == None) # assert all events are consummed
    if evt_receiver == None: evt_receiver = []
    EventFilterPretty(evt_receiver).filter(events)
    return evt_receiver


def events_from_obj(root, evt_receiver=None):
    """
    Creates an XML events stream from plain object.

    Generates an XML event stream suitable for xml_from_events() from
    a well formed XML plain object and pass it through the append()
    method to the receiver or to a newly created list.

    :param root: root of the XML plain object
    :param evt_receiver: the receiver implementing the append method or None

    :return: the receiver if not None or the created events list

    .. seealso: xml_from_events()
    """
    class EventGenerator():
        def __init__(self, evt_receiver):
            self.evt_receiver = evt_receiver
        def gen_content(self, token):
            self.evt_receiver.append(('|', (token,)))
        def gen_elt(self, name, children):
            self.evt_receiver.append(('<', (name,)))
            self.gen_attrs_or_elts(children)
            self.evt_receiver.append(('>', (name,)))
        def gen_attr(self, name, value):
            self.evt_receiver.append(('@', (name, value)))
        def gen_attr_or_elt(self, name, children):
            if name[0] == "@":
                self.gen_attr(name[1:], children)
            else:
                self.gen_elt(name, children)
        def gen_attrs_or_elts(self, elts):
            if isinstance(elts, list):
                for elt in elts: self.gen_attrs_or_elts(elt)
            elif isinstance(elts, dict):
                for name, children in elts.items(): self.gen_attr_or_elt(name, children)
            else: self.gen_content(elts)
        def generate_from(self, root):
            assert(isinstance(root, dict))
            assert(len(root.items()) == 1)
            (name, children) = list(root.items())[0]
            self.evt_receiver.append(('[', ("",)))
            self.gen_elt(name, children)
            self.evt_receiver.append((']', ("",)))
    if evt_receiver == None: evt_receiver = []
    EventGenerator(evt_receiver).generate_from(root)
    return evt_receiver


def xml_from_obj(root, outf=sys.stdout, encoding='UTF-8', pretty=True, indent="  "):
    """
    Generate a XML file from an XML plain object

    Generates to the given stream the validated XML output for the
    plain object. This function does the opposite of xml_to_obj().

    :param root: the root of the plain object
    :param outf: the output file stream
    :param encoding: the encoding to be used (default to "UTF-8")
    :param pretty: does indentation when True
    :param indent: base indent string (default to 2-space)

    .. seealso xml_to_obj()
    """
    evts = events_from_obj(root)
    if pretty: evts = events_filter_pretty(evts, indent=indent)
    xml_from_events(evts, outf, encoding=encoding)


def obj_to_yaml(root, stream=None):
    """
    Output an XML plain object to yaml.

    Output an object to yaml with some specific
    management for OrderedDict, Strings and Tuples.
    The specific treatment for these objects are
    there in order to preserve the XML ordered structure
    while generating a bare yaml file without any python object.

    Note that reading back the emitted YAML object should be done
    though obj_from_yaml() in order to preserve dict order.

    To be used as an alternative to a bare yaml.dump if one
    needs an editable YAML view of the XML plain object.

    :param root: root of the plain object to dump
    :stream: optional stream or None for generating a string
    :return: None or the generated string if stream is None
    """
    def dict_representer(dumper, data):
        return dumper.represent_dict(data.items())
    def tuple_representer(dumper, data):
        return dumper.represent_list(list(data))
    def str_presenter(dumper, data):
        if data.find('\n') >= 0:  # check for strings with newlines
            return dumper.represent_scalar(
                'tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    yaml.add_representer(OrderedDict, dict_representer)
    yaml.add_representer(str, str_presenter)
    if sys.hexversion < 0x03000000: yaml.add_representer(unicode, str_presenter)
    yaml.add_representer(tuple, tuple_representer)

    return yaml.dump(root, stream, allow_unicode=True, default_flow_style=False)


def obj_from_yaml(stream):
    """
    Read a YAML object, possibly holding a XML plain object.

    Returns the XML plain obj from the YAML stream or string.
    The dicts read from the YAML stream are stored as
    OrderedDict such that the XML plain object elements
    are kept in order.

    :param stream: input YMAL file stream or string
    :return: the constructed plain object
    """
    # load in ordered dict to keep fields ordered
    # https://stackoverflow.com/a/21912744
    class OrderedLoader(yaml.Loader): pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)



if __name__ == "__main__":
    import argparse, sys, os
    if "--doctest" in sys.argv:
        import doctest
        os.chdir(os.path.dirname(__file__))
        test = doctest.testmod()
        if test.failed == 0:
            print("SUCCESS: test python documentation")
            sys.exit(0)
        else:
            print("FAILED: test python documentation")
            sys.exit(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("--doctest", action="store_true", help="run documentation tests")
    parser.add_argument("--inf", default="xml", help="input format, one of: xml, yml, evt (default: xml)")
    parser.add_argument("--outf", default="xml", help="output format, one of: xml, yml, evt, py (default: xml)")
    parser.add_argument("--pretty", action='store_true', help="pretty parse/unparse")
    parser.add_argument("--filter", default="obj", help="intermefdiate filter, one of: obj, evt (default: obj)")
    parser.add_argument("input", nargs='?', help="input file or stdin")
    parser.add_argument("output", nargs='?', help="output file or stdout")
    args = parser.parse_args()
    if args.inf not in ["xml", "yml"]: parser.exit(2, "%s: error: argument to --inf is invalid\n" % parser.prog)
    if args.outf not in ["xml", "yml", "evt", "py"]: parser.exit(2, "%s: error: argument to --outf is invalid\n" % parser.prog)
    if args.filter not in ["obj", "evt"]: parser.exit(2, "%s: error: argument to --filter is invalid\n" % parser.prog)
    if args.filter == "evt" and args.inf not in ["xml"]: parser.exit(2, "%s: error: input format incompatible withg filter\n" % parser.prog)
    if args.filter == "evt" and args.outf not in ["xml", "evt"]: parser.exit(2, "%s: error: output format incompatible withg filter\n" % parser.prog)
    if args.input == None or args.input == "-": args.input = sys.stdin
    else: args.input = open(args.input)
    if args.output == None  or args.output == "-": args.output = sys.stdout
    else: args.output = open(args.output, "w")

    if args.inf == "xml":
        if args.filter == "evt": evts = xml_to_events(args.input)
        else: root = xml_to_obj(args.input, strip_space=args.pretty, fold_dict=args.pretty)
    elif args.inf == "yml": root = obj_from_yaml(args.input)
    if args.outf == "xml":
        if args.filter == "evt":
            xml_from_events(evts, args.output)
        else:
            xml_from_obj(root, args.output, pretty=args.pretty)
    elif args.outf == "yml": obj_to_yaml(root, args.output)
    elif args.outf == "py": args.output.write(str(root))
    elif args.outf == "evt":
        if args.filter == "obj":
            evts = events_from_obj(root)
        args.output.write(obj_to_yaml(evts))
