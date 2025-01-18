from textnode import TextNode, TextType

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


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
