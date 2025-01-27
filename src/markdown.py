import delimiter
import os   
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
        elif block_to_lines[i].startswith(f"{(i + 1)}. ") and ordered_list:
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
    if block_type == PARAGRAPH_BLOCK: 
        return md_paragraph_to_html(block)
    if block_type == CODE_BLOCK:    
        return md_code_to_html(block)
    if block_type == HEADING_BLOCK:
        return md_heading_to_html(block)
    else:
        raise Exception("incorrect block type")

def normal_to_children(text_nodes):
    children = []
    for text_node in text_nodes:
        children.append(text_node.text_node_to_html_node())
    return children

def md_paragraph_to_html(block):
    text_nodes = delimiter.text_to_textnodes(block)
    children = normal_to_children(text_nodes) 
    return ParentNode("p", children)

def md_ul_to_html(block):
    children = []
    block_lines = block.splitlines()
    for line in block_lines:
        if not (line.startswith("- ") or line.startswith("* ")):
            raise Exception("malformed unordered list")
        li_child = normal_to_children(delimiter.text_to_textnodes(line[2:len(line)]))
        children.append(ParentNode("li", li_child))
    return ParentNode("ul", children)

def md_ol_to_html(block):
    children = []
    block_lines = block.splitlines()
    for i in range(0, len(block_lines)):
        if not block_lines[i].startswith(f"{(i + 1)}. "):
            raise Exception("malformed ordered list")
        li_child = normal_to_children(delimiter.text_to_textnodes(block_lines[i][3:len(block_lines[i])]))
        children.append(ParentNode("li", li_child))
    return ParentNode("ol", children)
    
def md_quote_to_html(block):
    block_lines = block.splitlines()
    text_tmp = []
    for line in block_lines:
        if not line.startswith(">"):
            raise Exception("malformed markdown quotes")
        text_tmp.append(line[1:len(line)].strip())
    text = '\n'.join(text_tmp)
    return LeafNode("blockquote", text)

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
    blocks = delimiter.markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:    
        nodes.append(block_to_html_node(block))
    return ParentNode("div", nodes)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as md_file:
        markdown_string = md_file.read()
    with open(template_path) as template_file:
        template_string = template_file.read()
    html_root_node = markdown_to_html_node(markdown_string)
    html_string = html_root_node.to_html()
    print(html_string)
    page_title = extract_title(markdown_string)
    template_string = template_string.replace("{{ Title }}", page_title)
    template_string = template_string.replace("{{ Content }}", html_string)
    with open(dest_path + "/index.html", "w") as f:
        f.write(template_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    files = os.listdir(dir_path_content)
    for file in files:
        filepath = os.path.join(dir_path_content, file)
        if os.path.isfile(filepath):
            generate_page(filepath, template_path, dest_dir_path)
        if os.path.isdir(filepath):
            dest_folder = os.path.join(dest_dir_path, file)
            os.mkdir(dest_folder)
            generate_pages_recursive(filepath, template_path, dest_folder) 
