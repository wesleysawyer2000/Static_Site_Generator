from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# Markdown to Blocks
# # It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings
def markdown_to_blocks(markdown):
    markdown_clean = re.sub(r"[ \t]+(?=\n)", "", markdown)
    markdown_clean = re.sub(r"(?<=\n)[ \t]+", "", markdown_clean)
    text_split = markdown_clean.split("\n\n")
    blocks = []
    for text in text_split:
        text = text.strip()
        if text:
            blocks.append(text)
    return blocks


# Block to Block Type
# # It takes markdown text and returns what type of block it is
def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    elif re.match(r"^```\n(.*?)\n```$", markdown, re.DOTALL):
        return BlockType.CODE
    elif re.match(r"^> ?.*(\n> ?.*)*$", markdown):
        return BlockType.QUOTE
    elif re.match(r"^- .*(\n- .*)*$", markdown):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^1.*", markdown):
        text_split = markdown.split(f"\n")
        i = 1
        for text in text_split:
            if not text.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH