# xmlplain

XML as plain object utility module

[![Build Status](https://secure.travis-ci.org/guillon/xmlplain.svg)](http://travis-ci.org/guillon/xmlplain)

## Synopsys

This module is a set of utility functions for parsing self-contained
XML input into plain list/dict/string types and emitting to/reading
from XML or YAML formats.

The motivating usage was to dump XML to YAML, manually edit
files as YAML, and emit XML output back.

Though this module can be used more simply to dump compatible plain
list/dict/string objects into XML or YAML for textual storage.

An XML file content when read to object and written back to XML has
all it's document strcuture and content preserved w.r.t. to
elements start/end and text content.
Though XML comments, document type specifications, external
entity definitions are discarded if present on input. External system
entities (i.e. inclusion of external files) are not supported
and generate an input error.

The input XML is just syntactically validated and does not validate
against any DTD or schema specification as the underlying backend
is the core xml.sax module.

The only and optional destructive transformation on the document
content is a `strip_space` option on reading (resp. `pretty` option
on writing) which can affect non-leaf text content (stripping
leading and trailing spaces).

The XML namespaces are ignored as there is no actual schema validation,
hence element, attribute names and namespaces URIs attributes
are passed and preserved as-is.

Note that there are alternative modules with nearly the same
functionality, but none of them provide all of:

- simple plain objects (dict, list, strings) dumped to/reloaded from XML
- preservation of semi-structured XML documents (tags duplicates,
  mixed text and tags) on input
- management of human-editable form through YAML bridge


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

Execute the following python code:

```python
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

```python
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

Or get to the online documentation at: https://guillon.github.io/xmlplain


## Install

The module is compatible with `python 2.6/2.7` and `python 3.x`.

For a local installation (installs to `$HOME/.local`) do:

    pip install --user xmlplain

This will install the last release and its dependencies in your user environment.

Optionally install at system level with:

    sudo pip install xmlplain


## Sources

Download this module archives from the releases at: https://github.com/guillon/xmlplain/releases

Or clone the source git repository at: https://github.com/guillon/xmlplain


## Installation from sources

Install first modules dependencies with:

    pip install --user setuptools PyYAML ordereddict


Either copy the `xmlplain.py` file somewhere or install it
with `setup.py`.

For a user local installation (installs to `$HOME/.local`) do:

    ./setup.py install --user


## Development

This module is delivered as part of a source tree with tests, in order
to run tests, do for instance:

    make -j16 check

With python coverage installed, one may check coverage of changes with:

    make -j16 coverage
	firefox tests/coverage/html/index.html

When check target pass and newly added code is covered,
please submit a pull request to https://github.com/guillon/xmlplain


## Documentation

The documentation is generated with `sphinx` as is:

	make doc
    firefox html/index.html

The online documentation is hosted at: https://guillon.github.io/xmlplain


## Release

The release process relies on the virtualenv tool, python2 and python3
being installed on the release host.

The release builds, tests, do coverage checks on both python2 and python3
then generates documentation and uploadable archives for PyPi.

Before Bumping a release be sure to update the `__version__` string
in `xmlplain.py` and commit it (no check is done against the version
in the release target).

Then Proceed as follow to prepare the release:

    make -j16 release

When all this passes locally, commit all and push to github
`next/master` branch in order to have travis checks running.
Verify travis status before proceeding further, for instance
from the travis command line with:

    travis branches

Once all is passed, and the `make -j16 release` target has been re-executed,
upload doc to github and packages to PyPI with:

    make release-upload

At this point the package version should be available on https://pypi.org/project/xmlplain
and the doc updated on https://guillon.github.io/xmlplain

One should check the proper installation on PyPi with:

    make -j16 release-check

Which will restart a release check, this time downloading from PyPI instead of using
the local sources.

After all is done, one should manually update the github with:

- Apply a tag `vx.y.z` matching the new release version and push it to github
- Go to github and finalize the tag promotion into a release with and at least upload
  also on in the github release the source archive `xmlplain-x.y.x.tar.gz` available
  on the just uploaded PyPi files: https://pypi.org/project/xmlplain/#files
- Optionally add some information and publish the release


## License

This is free and unencumbered software released into the public domain.
