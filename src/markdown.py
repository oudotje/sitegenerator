def block_to_block_type(block):
    block_to_lines = block.splitlines()
    prefix_heading = []

    for i in range(1, 7):
        prefix_heading.append(f"{'#' * i} ")
    if block.startswith(tuple(prefix_heading)):
        return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
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
        return "quote"
    if unordered_list: 
        return "unordered_list"
    if ordered_list: 
        return "ordered_list"
    return "paragraph"
