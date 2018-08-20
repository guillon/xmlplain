# xmlplain
XML as plain object utility module

## Synopsys

This module is a set of utility functions for parsing XML input
into plain list/dict/string types.

These plain XML objects in turn can be emitted through YAML
for instance as bare YAML without python objects.

The motivating usage is to dump XML to YAML, manually edit
files as YAML, and emit XML output back.

The original XML file is supposed to be preserved except
for comments and (if requested) spaces between non-leaf elements.

Note that there are alternative modules with nearly the same
functionality, but none of them both provide simple plain objects
and preserve the initial XML content even for non structured XML.

WARNING: the implementation does not support XML namespaces
and entity location. If this is found useful, please add an issue.


## Usage

In order to convert a XML file to a YAML representation, for instance given
the `tests/example-1.xml` file:

```xml
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
```

Execute the following python3 code:

```python3
import xmlplain

# Read to plain object
with open("tests/example-1.xml") as inf:
  root = xmlplain.xml_to_obj(inf, strip_space=True, fold_dict=True)

# Output plain YAML
with open("example-1.yml", "w") as outf:
  xmlplain.obj_to_yaml(root, outf)
```

This will output the YAML representation in `example-1.yml`:

```yaml
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
```

One can then read the emitted YAML representation and generate
again an XML output with:

```python3
import xmlplain

# Read the YAML file
with open("example-1.yml") as inf:
  root = xmlplain.obj_from_yaml(inf)

# Output back XML
with open("example-1.new.xml", "w") as outf:
  xmlplain.xml_from_obj(root, outf, pretty=True)
```

This will output back the following XML (there may be some
indentation and/or short empty elements differences w.r.t. the
original):

```xml
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
```

For a detailled usage, read the API documentation with:

    pydoc xmlplain


## Installation

Either copy the `xmlplain.py` file somewhere or install it
with `setup.py`.

For a user local installation (installs to `$HOME/.local`) do:

    ./setup.py install --user

For a system level installtion do:

    ./setup.py build
    sudo ./setup.py install


## Unitary tests

This module is delivered as part of a source tree with tests, in order
to run tests, do for instance:

    make -j16 check


## License

This is free and unencumbered software released into the public domain.
