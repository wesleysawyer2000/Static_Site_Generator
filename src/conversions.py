import re
from textnode import *
from htmlnode import *
from block import *

# Text Node to HTML Node
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("ERROR: Invalid Text Type")

# Text to Children
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    node_list = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        node_list.append((html_node))
    return node_list

# Markdown to Text Node
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_split = node.text.split(delimiter)
        if len(node_split) % 2 == 0:
            raise Exception("ERROR: Invalid markdown syntax")
        for index, split in enumerate(node_split):
            if split == "":
                continue
            elif index % 2 == 0:
                new_nodes.append(TextNode(split, TextType.TEXT))
            else:
                new_nodes.append(TextNode(split, text_type))
    return new_nodes

# Markdown to Text Node (Images)
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        extract = extract_markdown_images(node.text)
        if not extract:
            new_nodes.append(node)
            continue
        for tup in extract:
            split_on = f"![{tup[0]}]({tup[1]})"
            text_split = current_text.split(split_on, 1) #
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(tup[0], TextType.IMAGE, tup[1]))
            current_text = text_split[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT)) #
    return new_nodes

# Markdown to Text Node (Links)
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        extract = extract_markdown_links(node.text)
        if not extract:
            new_nodes.append(node)
            continue
        for tup in extract:
            split_on = f"[{tup[0]}]({tup[1]})"
            text_split = current_text.split(split_on, 1) #
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(tup[0], TextType.LINK, tup[1]))
            current_text = text_split[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT)) #
    return new_nodes

# Text to TextNodes (Calls on: split_nodes_delimiter, split_nodes_image, split_nodes_link)
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


# Markdown to HTML Node
# # converts a full markdown document into a single parent HTMLNode
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_list = []
    for block_val in blocks:
        block_tag = None
        block_props = None
        block_type = block_to_block_type(block_val)
        if block_type == BlockType.HEADING:
            if block_val[0:6] == "######":
                block_tag = "h6"
            elif block_val[0:5] == "#####":
                block_tag = "h5"
            elif block_val[0:4] == "####":
                block_tag = "h4"
            elif block_val[0:3] == "###":
                block_tag = "h3"
            elif block_val[0:2] == "##":
                block_tag = "h2"
            else:
                block_tag = "h1"
            block_val = re.sub(r"^#+\s*", "", block_val)
        elif block_type == BlockType.CODE:
            block_tag = "code"
            lines = block_val.split("\n")
            block_val = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(text=block_val, text_type=TextType.TEXT)
            child = text_node_to_html_node(text_node)
            child_html_node = ParentNode(tag=block_tag, children=[child], props=block_props)
            parent_code_html_node = ParentNode(tag="pre", children=[child_html_node], props=None)
            child_list.append(parent_code_html_node)
            continue
        elif block_type == BlockType.QUOTE:
            block_tag = "blockquote"
            block_val = re.sub(r"(^>|\n>) ?", "", block_val)
            block_val = block_val.replace(f"\n", " ")
        elif block_type == BlockType.UNORDERED_LIST:
            block_tag = "ul"
            block_split = block_val.split(f"\n")
            list_items = []
            for split in block_split:
                split = re.sub(r"^(\*|-)\s*", "", split)
                children = text_to_children((split))
                parent_list_html_node = ParentNode(tag="li", children=children, props=None)
                list_items.append(parent_list_html_node)
            parent_code_list_node = ParentNode(tag=block_tag, children=list_items, props=None)
            child_list.append(parent_code_list_node)
            continue
        elif block_type == BlockType.ORDERED_LIST:
            block_tag = "ol"
            block_split = block_val.split(f"\n")
            list_items = []
            for split in block_split:
                split = re.sub(r"^\d+\.\s*", "", split)
                children = text_to_children((split))
                parent_list_html_node = ParentNode(tag="li", children=children, props=None)
                list_items.append(parent_list_html_node)
            parent_code_list_node = ParentNode(tag=block_tag, children=list_items, props=None)
            child_list.append(parent_code_list_node)
            continue
        else:
            block_tag = "p"
            block_val = block_val.replace(f"\n", " ")
        children = text_to_children(block_val)
        child_html_node = ParentNode(tag=block_tag, children=children, props=block_props)
        child_list.append(child_html_node)
    parent_html_node = ParentNode(tag="div", children=child_list, props=None)
    return parent_html_node
