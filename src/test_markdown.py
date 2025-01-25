import unittest
import markdown

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
        ordered = ". First point\n.. Second point\n... Third point\n.... Fourth point"
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
