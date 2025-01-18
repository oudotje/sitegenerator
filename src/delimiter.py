from textnode import TextNode, TextType
import re

def split_nodes(func, img=0):
    def wrapper(old_nodes):
        if old_nodes == []:
            raise ValueError("List of nodes should not be empty")
        
        new_nodes = []
        for node in old_nodes: 
            markdown = func(node.text)
            if markdown == []:
                new_nodes.append(node)
            else:
                node_text = node.text
                for md in markdown:
                    alt_txt = md[0]
                    link = md[1]
                    if img == 1: 
                        splitted_text = node_text.split(f"![{alt_txt}]({link})", maxsplit = 1)
                    else:
                        splitted_text = node_text.split(f"[{alt_txt}]({link})", maxsplit = 1)
                    new_nodes.append(TextNode(splitted_text[0], TextType.NORMAL))
                    if len(splitted_text) != 1:
                        if img == 1:
                            new_nodes.append(TextNode(alt_txt, TextType.IMAGES, link))
                        else:
                            new_nodes.append(TextNode(alt_txt, TextType.LINKS, link))
                        node.text = splitted_text[1]
        return new_nodes
    return wrapper

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes == []:
      raise ValueError("List of nodes should not be empty")

    new_nodes = []
    for node in old_nodes:
        if delimiter not in node.text:
            new_nodes.append(delimiter)
        else:
            splitted_text = node.text.split(delimiter)
            if len(splitted_text) % 2 == 0:
                raise Exception("Delimiter is not terminated, invalid MD syntax.")

            for i in range(0, len(splitted_text)):
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
