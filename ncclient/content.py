# Copyright 2009 Shikhar Bhushan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"TODO: docstring"

from xml.etree import cElementTree as ET


### Namespace-related ###

BASE_NS = 'urn:ietf:params:xml:ns:netconf:base:1.0'
# and this is BASE_NS according to cisco devices...
CISCO_BS = 'urn:ietf:params:netconf:base:1.0'

try:
    register_namespace = ET.register_namespace
except AttributeError:
    def register_namespace(prefix, uri):
        from xml.etree import ElementTree
        # cElementTree uses ElementTree's _namespace_map, so that's ok
        ElementTree._namespace_map[uri] = prefix

# we'd like BASE_NS to be prefixed as "netconf"
register_namespace('netconf', BASE_NS)

qualify = lambda tag, ns=BASE_NS: '{%s}%s' % (ns, tag)

# i would have written a def if lambdas weren't so much fun
multiqualify = lambda tag, nslist=(BASE_NS, CISCO_BS): [qualify(tag, ns)
                                                        for ns in nslist]

unqualify = lambda tag: tag[tag.rfind('}')+1:]

def namespaced_find(ele, tag, workaround=True):
    """`workaround` is for Cisco implementations (at least the one tested), 
    which uses an incorrect namespace.
    """
    found = None
    if not workaround:
        found = ele.find(tag)
    else:
        for qname in multiqualify(tag):
            found = ele.find(qname)
            if found is not None:
                break
    return found


### Build XML using Python data structures ###

class XMLConverter:
    """Build an ElementTree.Element instance from an XML tree specification
    based on nested dictionaries. TODO: describe spec
    """
    
    def __init__(self, spec):
        "TODO: docstring"
        self._root = XMLConverter.build(spec)
    
    def tostring(self, encoding='utf-8'):
        "TODO: docstring"
        xml = ET.tostring(self._root, encoding)
        # some etree versions don't include xml decl with utf-8
        # this is a problem with some devices
        return (xml if xml.startswith('<?xml')
                else '<?xml version="1.0" encoding="%s"?>%s' % (encoding, xml))
    
    @property
    def tree(self):
        "TODO: docstring"
        return self._root
    
    @staticmethod
    def build(spec):
        "TODO: docstring"
        if iselement(spec):
            return spec
        elif isinstance(spec, basestring):
            return ET.XML(spec)
        # assume isinstance(spec, dict)
        if 'tag' in spec:
            ele = ET.Element(spec.get('tag'), spec.get('attributes', {}))
            ele.text = spec.get('text', '')
            ele.tail = spec.get('tail', '')
            subtree = spec.get('subtree', [])
            # might not be properly specified as list but may be dict
            if isinstance(subtree, dict):
                subtree = [subtree]
            for subele in subtree:
                ele.append(XMLConverter.build(subele))
            return ele
        elif 'comment' in spec:
            return ET.Comment(spec.get('comment'))
        # TODO elif DOM rep
        else:
            raise ContentError('Invalid tree spec')
    
    @staticmethod
    def fromstring(xml):
        return XMLConverter.parse(ET.fromstring(xml))
    
    @staticmethod
    def parse(root):
        return {
            'tag': root.tag,
            'attributes': root.attrib,
            'text': root.text,
            'tail': root.tail,
            'subtree': [ XMLConverter.parse(child) for child in root.getchildren() ]
        }

## utility functions

iselement = ET.iselement

def isdom(x): return True # TODO

def root_ensured(rep, tag):
    if isinstance(rep, basestring):
        rep = ET.XML(rep)
    err = False
    if ((iselement(rep) and (rep.tag not in (tag, qualify(tag))) or (isdom(x)))): 
        raise ArgumentError("Expected root element [%s] not found" % tag)
    else:
        return rep