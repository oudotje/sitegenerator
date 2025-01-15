import unittest
import delimiter
from textnode import TextType, TextNode

class TestDelimiter(unittest.TestCase):
    def test_emptylist(self):
        self.assertRaises(ValueError, delimiter.split_nodes_delimiter, [], "'", TextType.NORMAL)
    
    def test_code_delimiter(self):
        node = TextNode("This is a text with a `code block` word", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_markdown_error(self):
        node = TextNode("This is a failed * markdown", TextType.NORMAL)
        self.assertRaises(Exception, delimiter.split_nodes_delimiter, [node], "*", TextType.ITALIC)

    def test_bold_delimiter(self):
        node = TextNode("This is a **bold** text", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_italic_delimiter(self):
        node = TextNode("This is an *italic* delimiter *and* this too", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text_type, TextType.NORMAL)

if __name__ == "__main__":
    unittest.main()
