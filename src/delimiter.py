from textnode import TextNode, TextType
import re

def split_nodes(func, img=0):
    def wrapper(old_nodes):
        if old_nodes == []:
            raise ValueError("List of nodes should not be empty")
        
        new_nodes = []
        for node in old_nodes: 
            if node.text_type != TextType.NORMAL:
                new_nodes.append(node)
                continue
            markdown = func(node.text)
            if markdown == []:
                new_nodes.append(node)
                continue 
            else:
                node_text = node.text
                for md in markdown:
                    if img == 1: 
                        splitted_text = node_text.split(f"![{md[0]}]({md[1]})", maxsplit = 1)
                    else:
                        splitted_text = node_text.split(f"[{md[0]}]({md[1]})", maxsplit = 1)
                    if len(splitted_text) == 1:
                        raise ValueError("The markdown link is broken")
                    new_nodes.append(TextNode(splitted_text[0], TextType.NORMAL))
                    if img == 1:
                        new_nodes.append(TextNode(md[0], TextType.IMAGES, md[1]))
                    else:
                        new_nodes.append(TextNode(md[0], TextType.LINKS, md[1]))
                    node_text = splitted_text[1]                    
                if node_text != "":
                    new_nodes.append(TextNode(node_text, TextType.NORMAL))
        return new_nodes
    return wrapper

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes == []:
      raise ValueError("List of nodes should not be empty")

    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        else:
            splitted_text = node.text.split(delimiter)
            if len(splitted_text) % 2 == 0:
                raise Exception("Delimiter is not terminated, invalid MD syntax.")

            for i in range(0, len(splitted_text)):
                if not splitted_text[i]:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(splitted_text[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    split_nodes_img = split_nodes(extract_markdown_images, 1)
    return split_nodes_img(old_nodes)

def split_nodes_link(old_nodes):
    split_nodes_lnk = split_nodes(extract_markdown_links)
    return split_nodes_lnk(old_nodes)

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text) 
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def text_to_textnodes(text):
    updated_text_nodes = [TextNode(text, TextType.NORMAL)]
    delimiters = {"**":TextType.BOLD, "*":TextType.ITALIC, "`":TextType.CODE}
    for delimiter in delimiters:
        updated_text_nodes = split_nodes_delimiter(updated_text_nodes, delimiter, delimiters[delimiter])
    updated_text_nodes = split_nodes_image(updated_text_nodes)
    updated_text_nodes = split_nodes_link(updated_text_nodes)
    return updated_text_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(filter(lambda x: x != "", blocks))
    blocks = list(map(str.strip, blocks))
    return blocks
