import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(None, node.url)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a test node", TextType.NORMAL)
        self.assertEqual(node.__repr__(), "TextNode(This is a test node, normal, None)")

    def test_to_html_normal(self):
        node = TextNode("normal", TextType.NORMAL)
        leaf = node.text_node_to_html_node()
        self.assertEqual(leaf.value, "normal")
        self.assertEqual(leaf.tag, None)
        self.assertEqual(leaf.props, None)

    def test_to_html_bold(self):
        node = TextNode("bold", TextType.BOLD)
        leaf = node.text_node_to_html_node()
        self.assertEqual(leaf.value, "bold")
        self.assertEqual(leaf.tag, "b")
        self.assertEqual(leaf.props, None)
        self.assertEqual(leaf.to_html(), "<b>bold</b>")

    def test_to_html_link(self):
        node = TextNode("link", TextType.LINKS, url="https://www.google.com")
        leaf = node.text_node_to_html_node()
        self.assertEqual(leaf.value, "link")
        self.assertEqual(leaf.tag, "a")
        self.assertEqual(leaf.props['href'], node.url)
        self.assertEqual(leaf.to_html(), "<a href=\"https://www.google.com\">link</a>")

    def test_to_html_imagae(self):
        node = TextNode("image", TextType.IMAGES, url="https://img.text")
        leaf = node.text_node_to_html_node()
        self.assertEqual(leaf.value, "")
        self.assertEqual(leaf.tag, "img")
        self.assertEqual(leaf.props['src'], "https://img.text")
        self.assertEqual(leaf.props['alt'], node.text)
        self.assertEqual(leaf.to_html(), "<img src=\"https://img.text\" alt=\"image\"></img>")

if __name__ == "__main__":
    unittest.main()
