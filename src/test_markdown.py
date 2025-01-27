import unittest
import markdown
from htmlnode import LeafNode, ParentNode

class TestMarkdown(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        heading = "Test"
        for i in range(1, 7):
            test_string = f"{'#' * i} " + heading
            block = markdown.block_to_block_type(test_string)
            self.assertEqual(block, "heading")
    
    def test_block_to_block_type_code(self):
        code = "```code block```"
        self.assertEqual(markdown.block_to_block_type(code), "code")

    def test_block_to_block_type_quote(self):
        quote = ">Quote 1\n>Quote 2"
        self.assertEqual(markdown.block_to_block_type(quote), "quote")

    def test_block_to_block_type_unordered(self):
        unordered = "* This is the first point\n- This the second point\n* Of an\n- Unordered list"
        self.assertEqual(markdown.block_to_block_type(unordered), "unordered_list")

    def test_block_to_block_type_ordered(self):
        ordered = "1. First point\n2. Second point\n3. Third point\n4. Fourth point"
        self.assertEqual(markdown.block_to_block_type(ordered), "ordered_list")

    def test_block_to_block_paragrah(self):
        paragraph1 = "This is a paragraph"
        paragraph2 = "```This is a paragraph``"
        paragraph3 = "#This is a paragraph"
        paragraph4 = ">This is a paragraph\n. Test"
        paragraph5 = "* This is a paragraph\n-Test"
        paragraph6 = ".This is a\n. Paragraph"
        paragraphs = [paragraph1, paragraph2, paragraph3, paragraph4, paragraph5, paragraph6]
        for paragraph in paragraphs:
            self.assertEqual(markdown.block_to_block_type(paragraph), "paragraph")
    
    def test_extract_title(self):
        title = "# Title"
        expected_result = "Title"
        self.assertEqual(markdown.extract_title(title), expected_result)
    
    def test_extract_title_exception(self):
        title = "Title"
        self.assertRaises(Exception, markdown.extract_title, title)

    def test_extract_title_multiline(self):
        title = "# Title\n\n## Title 2\n\n ### Title 3\nSome text"
        expected_result = "Title"
        self.assertEqual(markdown.extract_title(title), expected_result)

    def test_md_headings_to_html(self):
        heading = "### My heading"
        obtained_result = markdown.md_heading_to_html(heading)
        expected_result = LeafNode("h3", "My heading")
        self.assertEqual(obtained_result.tag, expected_result.tag)
        self.assertEqual(obtained_result.value, expected_result.value)
    
    def test_md_headings_to_html_repr(self):
        heading = "### My heading"
        obtained_result = markdown.md_heading_to_html(heading)
        expected_result = LeafNode("h3", "My heading")
        self.assertEqual("<h3>My heading</h3>", expected_result.to_html())
        
    def test_md_headings_to_html_exception(self):
        heading = "#####"
        self.assertRaises(Exception, markdown.md_heading_to_html, heading)

    def test_md_code_to_html(self):
        code = "```code block```"
        obtained_result = markdown.md_code_to_html(code)
        expected_result = LeafNode("code", "code block")
        self.assertEqual(obtained_result.tag, expected_result.tag)
        self.assertEqual(obtained_result.value, expected_result.value)

    def test_md_code_to_html_exception(self):
        code = "``code block```"
        self.assertRaises(Exception, markdown.md_code_to_html, code)
    
    def test_md_code_to_html_longblock(self):
        code = "````code block```"
        obtained_result = markdown.md_code_to_html(code)
        expected_result = LeafNode("code", "`code block")
        self.assertEqual(obtained_result.tag, expected_result.tag)
        self.assertEqual(obtained_result.value, expected_result.value)

    def test_md_code_to_html_repr(self):
        code = "```code block```"
        obtained_result = markdown.md_code_to_html(code)
        expected_repr = "<code>code block</code>"
        self.assertEqual(obtained_result.to_html(), expected_repr) 

    def test_md_quote_to_html(self):
        quote = ">Quote1\n>Quote2\n>Quote3"
        obtained_result = markdown.md_quote_to_html(quote)
        expected_result = LeafNode("blockquote", "Quote1\nQuote2\nQuote3")
        self.assertEqual(obtained_result.tag, expected_result.tag)
        self.assertEqual(obtained_result.value, obtained_result.value)

    def test_md_quote_to_html_repr(self):
        quote = ">Quote1\n>Quote2\n>Quote3"
        obtained_result = markdown.md_quote_to_html(quote)
        expected_result = "<blockquote>Quote1\nQuote2\nQuote3</blockquote>"
        self.assertEqual(obtained_result.to_html(), expected_result)

    def test_md_quote_to_html_exception(self):
        quote = ">Quote1\nQuote2\n>Quote3"
        self.assertRaises(Exception, markdown.md_quote_to_html, quote)

    def test_md_ul_to_html(self):
        unordered_list = "* Item 1 is *italic*\n- Item 2"
        obtained_result = markdown.md_ul_to_html(unordered_list)
        item_1 = ParentNode("li", [LeafNode(None, "Item 1 is "), LeafNode("i", "italic")])
        item_2 = ParentNode("li", [LeafNode(None, "Item 2")])
        children = [item_1, item_2] 
        expected_result = ParentNode("ul", children)
        self.assertEqual(type(obtained_result), type(expected_result))
        self.assertEqual(len(obtained_result.children), len(expected_result.children))
        self.assertEqual(obtained_result.tag, expected_result.tag)
        for i in range(0, len(obtained_result.children)):
            self.assertEqual(obtained_result.children[i].tag, expected_result.children[i].tag)
            self.assertEqual(obtained_result.children[i].value, expected_result.children[i].value)

    def test_md_ul_to_html_exception(self):
        unordered_list = "> Item 1\n* Item 2"
        self.assertRaises(Exception, markdown.md_ul_to_html, unordered_list)

    def test_md_ul_to_html_repr(self):
        unordered_list = "* Item 1\n- Item 2"
        obtained_result = markdown.md_ul_to_html(unordered_list)
        expected_result = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        self.assertEqual(obtained_result.to_html(), expected_result)

    def test_md_ol_to_html(self):
        ordered_list = "1. Item 1\n2. Item 2\n3. Item 3"
        obtained_result = markdown.md_ol_to_html(ordered_list)
        item_1 = ParentNode("li", LeafNode(None, "Item 1"))
        item_2 = ParentNode("li", LeafNode(None, "Item 2"))
        item_3 = ParentNode("li", LeafNode(None, "Item 3"))
        expected_result = ParentNode("ol", [item_1, item_2, item_3])
        self.assertEqual(len(obtained_result.children), len(expected_result.children))
        self.assertEqual(obtained_result.tag, expected_result.tag)
        for i in range(0, len(expected_result.children)):
            self.assertEqual(obtained_result.children[i].tag, expected_result.children[i].tag)
            self.assertEqual(obtained_result.children[i].value, expected_result.children[i].value)

    def test_md_ol_to_html_exception(self):
        ordered_list = "1.Item 1\n2. Item 2"
        self.assertRaises(Exception, markdown.md_ol_to_html, ordered_list)

    def test_md_ol_to_html_repr(self):
        ordered_list = "1. Item 1\n2. Item 2\n3. Item 3"
        obtained_result = markdown.md_ol_to_html(ordered_list).to_html()
        expected_result = "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
        self.assertEqual(obtained_result, expected_result)

    def test_md_paragraph_to_html(self):
        md_test = "Normal and **bold** and *italic* and `code` and ![image](http://image.com) and [link](link.com) hello"
        normal_node = LeafNode(None, "Normal and ")
        bold_node = LeafNode("b", "bold")
        normal_node2 = LeafNode(None, " and ")
        italic_node = LeafNode("i", "italic")
        normal_node3 = LeafNode(None, " and ")
        code_node = LeafNode("code", "code")
        normal_node4 = LeafNode(None, " and ")
        image_node = LeafNode("img", "", {"src":"http://image.com", "alt":"image"})
        normal_node5 = LeafNode(None, " and ")
        link_node = LeafNode("a", "link", {"href":"link.com"})
        normal_node6 = LeafNode(None, " hello")
        children = [normal_node, bold_node, normal_node2, italic_node, normal_node3, code_node, normal_node4, image_node, normal_node5, link_node, normal_node6]
        root_node = ParentNode("p", children)
        obtained_result = markdown.md_paragraph_to_html(md_test)
        self.assertEqual(type(obtained_result), type(root_node))
        self.assertEqual(obtained_result.tag, root_node.tag)
        self.assertEqual(len(obtained_result.children), len(root_node.children))
        for i in range(0, len(obtained_result.children)):
            self.assertEqual(obtained_result.children[i].value, root_node.children[i].value)
            self.assertEqual(obtained_result.children[i].tag, root_node.children[i].tag)

    def test_markdown_to_html_quote(self):
        quote = ">Item 1\n>Item 2"
        obtained_result = markdown.markdown_to_html_node(quote)
        children = [LeafNode("blockquote", "Item 1\nItem 2")]
        expected_result = ParentNode("div", children)
        self.assertEqual(type(obtained_result), type(expected_result))
        self.assertEqual(obtained_result.tag, expected_result.tag)
        self.assertEqual(len(obtained_result.children), len(expected_result.children))
        for i in range(0, len(obtained_result.children)):
            self.assertEqual(obtained_result.children[i].tag, expected_result.children[i].tag)
            self.assertEqual(obtained_result.children[i].value, expected_result.children[i].value)

    def test_markdown_to_html_code(self):
        code = "```code block```"
        obtained_result = markdown.markdown_to_html_node(code)
        children = [LeafNode("code", "code block")]
        expected_result = ParentNode("div", children)
        self.assertEqual(type(obtained_result), type(expected_result))
        self.assertEqual(len(obtained_result.children), len(expected_result.children))
        self.assertEqual(obtained_result.tag, expected_result.tag)
        for i in range(0, len(obtained_result.children)):
            self.assertEqual(obtained_result.children[i].tag, expected_result.children[i].tag)
            self.assertEqual(obtained_result.children[i].value, expected_result.children[i].value) 

    def test_markdown_to_html_paragraph(self):
        paragraph = "This is a `code block` and an *italic text*"
        normal_node1 = LeafNode(None, "This is a ")
        code_node = LeafNode("code", "code block")
        normal_node2 = LeafNode(None, " and an ")
        italic_node = LeafNode("i", "italic text")
        children = [normal_node1, code_node, normal_node2, italic_node]
        expected_result = ParentNode("div", [ParentNode("p", children)])
        obtained_result = markdown.markdown_to_html_node(paragraph)
        self.assertEqual(type(obtained_result), type(expected_result))
        self.assertEqual(obtained_result.children[0].tag, expected_result.children[0].tag)
        self.assertEqual(len(obtained_result.children[0].children), len(expected_result.children[0].children))
        self.assertEqual(obtained_result.tag, expected_result.tag)
        for i in range(0, len(obtained_result.children[0].children)):
            expected_node = expected_result.children[0].children[i]
            obtained_node = obtained_result.children[0].children[i]
            self.assertEqual(expected_node.tag, obtained_node.tag)
            self.assertEqual(expected_node.value, obtained_node.value)
