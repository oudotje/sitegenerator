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

    def test_notexist_delimiter(self):
        node = TextNode("This is an **italic** delimiter", TextType.NORMAL)
        node1 = TextNode("img", TextType.IMAGES, "img.com")
        new_nodes = delimiter.split_nodes_delimiter([node, node1], ",", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is an **italic** delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "img")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[1].url, "img.com")

    def test_extract_markdown_images(self):
        text = "This is a text with a ![text](https://test) and another ![test](http://hello)"
        images = delimiter.extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("text", "https://test"))

    def test_extract_markdown_images_fail(self):
        text = "This is a text with a [text](hello) failed matching!"
        images = delimiter.extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_extract_markdown_images_empty(self):
        text = "This is a text with no images"
        images = delimiter.extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_extract_markdown_links(self):
        text = "This is a text with two markdown links [hello](test) and [hello1](test2)"
        links = delimiter.extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("hello", "test"))
        self.assertEqual(links[1], ("hello1", "test2"))

    def test_extract_markdown_links_fail(self):
        text = "This is a text with a broken [link(test)"
        links = delimiter.extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_extract_markdown_links_empty(self):
        text = "This is a text with no link"
        links = delimiter.extract_markdown_links(text)
        self.assertEqual(len(links), 0)

    def test_split_nodes_images(self):
        node = TextNode( "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL,)
        new_nodes = delimiter.split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
 
    def test_split_nodes_images_multi(self):
        node1 = TextNode("This is a text with image ![test](https://)", TextType.NORMAL)
        node2 = TextNode("This is a second image ![test2](image)", TextType.NORMAL)
        node3 = TextNode("[img](test_img)", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_image([node1, node2, node3])
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is a text with image ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "test2")
        self.assertEqual(new_nodes[3].url, "image")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGES)

    def test_split_nodes_images_empty(self):
        self.assertRaises(ValueError, delimiter.split_nodes_image, [])

    def test_split_nodes_images_no_image(self):
        node = TextNode("This is a normal text node!", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_images_no_text(self):
        node = TextNode("This is a [test](link) node", TextType.LINKS)
        new_nodes = delimiter.split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_links(self):
        node = TextNode("This is text with a link [hello](link) and [yes](it) and [no](then)", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_link([node])
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "yes")
        self.assertEqual(new_nodes[3].url, "it")
        self.assertEqual(new_nodes[3].text_type, TextType.LINKS)

    def test_split_nodes_links_second(self):
        node = TextNode("an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)

    def test_split_nodes_links_empty(self):
        self.assertRaises(ValueError, delimiter.split_nodes_link, [])

    def test_split_nodes_links_no_link(self):
        node = TextNode("There is no link in this node!", TextType.NORMAL)
        new_nodes = delimiter.split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_links_no_text(self):
        node = TextNode("This node is not a **text** node", TextType.ITALIC)
        new_nodes = delimiter.split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_nodes_links_invalid(self):
        node = TextNode("This node contains an invalid ![node(test)", TextType.NORMAL)
        self.assertRaises(Exception, delimiter.split_nodes_link, node)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_to_nodes = delimiter.text_to_textnodes(text)
        expected_result = [TextNode("This is ", TextType.NORMAL), TextNode("text", TextType.BOLD), 
                           TextNode(" with an ", TextType.NORMAL), TextNode("italic", TextType.ITALIC),
                           TextNode(" word and a ", TextType.NORMAL), TextNode("code block", TextType.CODE),
                           TextNode(" and an ", TextType.NORMAL), TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
                           TextNode(" and a ", TextType.NORMAL), TextNode("link", TextType.LINKS, "https://boot.dev")]
        self.assertEqual(len(expected_result), len(text_to_nodes))
        for i in range(0, len(text_to_nodes)):
            self.assertEqual(text_to_nodes[i].text_type, expected_result[i].text_type)
            self.assertEqual(text_to_nodes[i].text, expected_result[i].text)

    def test_text_to_textnodes_empty(self):
        text = ""
        text_to_nodes = delimiter.text_to_textnodes(text)
        expected_result = [TextNode("", TextType.NORMAL)]
        self.assertEqual(len(text_to_nodes), len(expected_result))
        self.assertEqual(text_to_nodes[0].text, expected_result[0].text)

    def test_text_to_textnodes_invalid(self):
        text = "This is a text with an invalid **bold text and a valid *italic* one"
        self.assertRaises(Exception, delimiter.text_to_textnodes, text)

    def test_text_to_textnodes_text(self):
        text = "This a raw markdown text"
        expected_result = [TextNode("This a raw markdown text", TextType.NORMAL)]
        text_to_nodes = delimiter.text_to_textnodes(text)
        self.assertEqual(len(expected_result), len(text_to_nodes))
        self.assertEqual(expected_result[0].text, text_to_nodes[0].text)
        self.assertEqual(expected_result[0].text_type, text_to_nodes[0].text_type)

    def test_markdown_to_blocks(self):
        markdown = "# This is a first block\n\n## This is a second block\n\n* This is a third block"
        expected_blocks = ["# This is a first block","## This is a second block", "* This is a third block"]
        resulting_blocks = delimiter.markdown_to_blocks(markdown)
        self.assertEqual(len(expected_blocks), len(resulting_blocks))
        for i in range(0, len(expected_blocks)):
            self.assertEqual(resulting_blocks[i], expected_blocks[i])

    def test_markdown_to_blocks_empty(self):
        markdown = ""
        expected_blocks = []
        resulting_blocks = delimiter.markdown_to_blocks(markdown)
        self.assertEqual(len(expected_blocks), len(resulting_blocks))

    def test_markdown_to_blocks_multinewlines(self):
        markdown = "# This is a first block\n\n\n## This is a second block\n\n"
        expected_blocks = ["# This is a first block", "## This is a second block"]
        resulting_blocks = delimiter.markdown_to_blocks(markdown)
        self.assertEqual(len(resulting_blocks), len(expected_blocks))
        for i in range(0, len(expected_blocks)):
            self.assertEqual(expected_blocks[i], resulting_blocks[i])

    def test_markdown_to_blocks_trailing(self):
        markdown = "   # This is a first block\n\n\n  ## This is a second block  "
        expected_blocks = ["# This is a first block", "## This is a second block"]
        resulting_blocks = delimiter.markdown_to_blocks(markdown)
        self.assertEqual(len(resulting_blocks), len(expected_blocks))
        for i in range(0, len(resulting_blocks)):
            self.assertEqual(expected_blocks[i], resulting_blocks[i])


if __name__ == "__main__":
    unittest.main()
