import delimiter
from textnode import TextNode
from htmlnode import LeafNode, ParentNode

QUOTE_BLOCK = "quote"
UO_LIST_BLOCK = "unordered_list"
O_LIST_BLOCK = "ordered_list"
PARAGRAPH_BLOCK = "paragraph"
HEADING_BLOCK = "heading"
CODE_BLOCK = "code"

def block_to_block_type(block):
    block_to_lines = block.splitlines()
    prefix_heading = []

    for i in range(1, 7):
        prefix_heading.append(f"{'#' * i} ")
    if block.startswith(tuple(prefix_heading)):
        return HEADING_BLOCK
    if block.startswith("```") and block.endswith("```"):
        return CODE_BLOCK
    
    quote_block = True
    unordered_list = True
    ordered_list = True
    for i in range(0, len(block_to_lines)):
        if block_to_lines[i].startswith(">") and quote_block:
            unordered_list = False
            ordered_list = False
        elif block_to_lines[i].startswith(tuple(["* ", "- "])) and unordered_list:
            quote_block = False
            ordered_list = False
        elif block_to_lines[i].startswith(f"{'.' * (i + 1)} ") and ordered_list:
            quote_block = False
            unordered_list = False
        else:
            quote_block = False
            unordered_list = False
            ordered_list = False
            break
    if quote_block: 
        return QUOTE_BLOCK
    if unordered_list: 
        return UO_LIST_BLOCK
    if ordered_list: 
        return O_LIST_BLOCK 
    return PARAGRAPH_BLOCK

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line.split("# ", 1)[1]
    raise Exception("missing title")

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == QUOTE_BLOCK:
        return md_quote_to_html(block)
    if block_type == UO_LIST_BLOCK:
        return md_ul_to_html(block)
    if block_type == O_LIST_BLOCK:
        return md_ol_to_html(block)
    if block_type == PARAGRAPH: 
        return md_paragraph_to_html(block) 
    if block_type == CODE_BLOCK:
        return md_code_to_html(block)
    if block_type == HEADING_BLOCK:
        return md_heading_to_html(block)

def md_paragraph_to_html(block):
    text_nodes = delimiter.text_to_textnodes(block)
    children = []
    for text_node in text_nodes:
        children.append(text_node.text_node_to_html_node())
    return ParentNode("p", children)

def md_ul_to_html(block):
    children = []
    block_lines = block.splitlines()
    for line in block_lines:
        if not (line.startswith("- ") or line.startswith("* ")):
            raise Exception("malformed unordered list")
        children.append(LeafNode("li", line[2:len(line)]))
    return ParentNode("ul", children)

def md_ol_to_html(block):
    children = []
    block_lines = block.splitlines()
    for i in range(0, len(block_lines)):
        if not block_lines[i].startswith(f"{'.' * (i + 1)} "):
            raise Exception("malformed ordered list")
        children.append(LeafNode("li", block_lines[i][i + 2:len(block_lines[i])]))
    return ParentNode("ol", children)
    

def md_quote_to_html(block):
    block_lines = block.splitlines()
    text_tmp = []
    for line in block_lines:
        if not line.startswith(">"):
            raise Exception("malformed markdown quotes")
        text_tmp.append(line[1:len(line)])
    text = '\n'.join(text_tmp)
    return LeafNode("q", text)

def md_heading_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level >= len(block):
        raise Exception("missing heading text")
    text = block[level + 1:]
    return LeafNode(f"h{level}", text)

def md_code_to_html(block):
    if not block.startswith("```") and block.endswith("```"):
        raise Exception("malformed code block")
    text = block[3:len(block) - 3]
    return LeafNode("code", text)

def markdown_to_html_node(markdown):
    blocks = delimiter.makrdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_html_node(block)

def generate_page(from_path, template_path):
    #print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        markdown_string = md_file.read()
    with open(template_path) as template_file:
        template_string = template_file.read()
    print(f"Markdown string: {markdown_string}\nTemplate string: {template_string}")
