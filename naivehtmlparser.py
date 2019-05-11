#!/usr/bin/env python
"""
Python 3.x HTMLParser extension with ElementTree support.
"""

from html.parser import HTMLParser
from xml.etree import ElementTree


class NaiveHTMLParser(HTMLParser):
    """
    Python 3.x HTMLParser extension with ElementTree support.
    @see https://github.com/marmelo/python-htmlparser
    """

    def __init__(self):
        self.root = None
        self.tree = []
        HTMLParser.__init__(self)

    def feed(self, data):
        HTMLParser.feed(self, data)
        return self.root

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        if len(self.tree) == 0:
            element = ElementTree.Element(tag, dict(self.__filter_attrs(attrs)))
            self.tree.append(element)
            self.root = element
        else:
            element = ElementTree.SubElement(self.tree[-1], tag, dict(self.__filter_attrs(attrs)))
            self.tree.append(element)

    def handle_endtag(self, tag):
        print("Encountered an end tag:", tag)
        self.tree.pop()

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)
        pass

    def handle_data(self, data):
        print("Encountered some data:", data)
        if self.tree:
            self.tree[-1].text = data

    def get_root_element(self):
        return self.root

    def __filter_attrs(self, attrs):
        return filter(lambda x: x[0] and x[1], attrs) if attrs else []

f = open("test1.html","r")
html = f.read()
print("\nINPUT")
print("------------------------")
print(html)
print("\n\nOUTPUT")
print("------------------------")

# example usage
if __name__ == "__main__":

    parser = NaiveHTMLParser()
    root = parser.feed(html)
    parser.close()

    print("\n")
    # root is an xml.etree.Element and supports the ElementTree API
    # (e.g. you may use its limited support for XPath expressions)

    # get title
    print(root.find('head/title').text)


    # get all anchors
    for a in root.findall('.//a'):
        print(a.get('href'))
    #print("\n")
    #for child in parser.root:
    #	print(child.tag, child.attrib)
    #print("\n")
    #print(parser.root)

    # for more information, see:
    # http://docs.python.org/2/library/xml.etree.elementtree.html
    # http://docs.python.org/2/library/xml.etree.elementtree.html#xpath-support
