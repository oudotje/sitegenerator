import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_init(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_empty_rep(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.__repr__(), "HTMLNode(None, None, None, None)")

    def test_init(self):
        html_node = HTMLNode("p", "test", [], {"href":"https://www.google.com"})
        self.assertEqual(html_node.tag, "p")
        self.assertEqual(html_node.value, "test")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props['href'], "https://www.google.com")

    def test_props_to_html(self):
        html_node = HTMLNode(props={"href":"https://www.google.com", "target":"_blank"})
        html_node_props_str = html_node.props_to_html()
        self.assertEqual(html_node_props_str, " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html_empty(self):
        html_node = HTMLNode("p", "test", [])
        self.assertEqual(html_node.props_to_html(), "")
       

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        leaf_node = LeafNode("p", "This is a paragraph")
        self.assertEqual(leaf_node.value, "This is a paragraph")
        self.assertEqual(leaf_node.tag, "p")
        self.assertEqual(leaf_node.props, None)
        self.assertEqual(leaf_node.children, None)

    def test_to_html_novalue(self):
        leaf_node = LeafNode("p", None)
        self.assertRaises(ValueError, leaf_node.to_html)

    def test_to_html_notag(self):
        leaf_node = LeafNode(None, "This is a test")
        self.assertEqual(leaf_node.to_html(), "This is a test")

    def test_to_html(self):
        leaf_node = LeafNode("a", "This is a test", {"href":"https://www.google.com"})
        self.assertEqual(leaf_node.to_html(), "<a href=\"https://www.google.com\">This is a test</a>")
     
