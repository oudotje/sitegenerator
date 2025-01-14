import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
    
class TestParentNode(unittest.TestCase):
    def test_init(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.tag, "p")
        self.assertEqual(parent_node.value, None)
        self.assertEqual(parent_node.children, [])
        self.assertEqual(parent_node.props, None)

    def test_to_html_emptychildren(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.to_html(), "<p></p>")


    def test_to_html_leafchildren(self):
        child1 = LeafNode("a","Click!", {"href":"https://www.google.com"})
        child2 = LeafNode(None, "This is normal text")
        child3 = LeafNode("i", "This is italic")
        parent_node = ParentNode("p", [child1, child2, child3], {"test":"test_props"})

        self.assertEqual(parent_node.to_html(), "<p test=\"test_props\"><a href=\"https://www.google.com\">Click!</a>This is normal text<i>This is italic</i></p>")

    def test_to_html_parentchildren(self):
        child1 = LeafNode("a", "Click!", {"href":"https://www.google.com"})
        parent1 = ParentNode("p", [child1])
        child2 = LeafNode("i", "This is italic")
        parent2 = ParentNode("p", [parent1, child2], {"test":"test"})

        self.assertEqual(parent2.to_html(), "<p test=\"test\"><p><a href=\"https://www.google.com\">Click!</a></p><i>This is italic</i></p>")

    def test_to_html_nonetag(self):
        parent_node = ParentNode(None, [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_nonechildren(self):
        parent_node = ParentNode("p", None)
        self.assertRaises(ValueError, parent_node.to_html)

if __name__ == "__main__":
    unittest.main()
