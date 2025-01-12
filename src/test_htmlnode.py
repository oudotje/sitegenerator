import unittest

from htmlnode import HTMLNode

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
        
