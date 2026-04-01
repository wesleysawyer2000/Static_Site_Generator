import unittest
import block
from conversions import *


class TestTextNode(unittest.TestCase):
    def test_textToHTMLtypeText(self):
        node = TextNode("This is a TEXT node", TextType.TEXT)
        node_html = text_node_to_html_node(node)
        leaf = LeafNode(None, "This is a TEXT node")
        self.assertEqual(node_html, leaf)

    def test_textToHTMLtypeBold(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        node_html = text_node_to_html_node(node)
        leaf = LeafNode("b", "This is a BOLD node")
        self.assertEqual(node_html, leaf)

    def test_textToHTMLtypeImage(self):
        node = TextNode("This is a IMAGE node", TextType.IMAGE, "https://www.boot.dev")
        node_html = text_node_to_html_node(node)
        leaf = LeafNode("img", "", {"src": "https://www.boot.dev", "alt": "This is a IMAGE node"})
        self.assertEqual(node_html, leaf)

    def test_MarkdownToHTMLtext(self):
        expected = [
            TextNode("This is text", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
            ]
        test = split_nodes_delimiter([TextNode("This is text", TextType.TEXT), TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)], "**", TextType.BOLD)
        self.assertEqual(expected, test, "ERROR: Markdown to HTML conversion not working")

    def test_MarkdownToHTMLbold(self):
        expected = [
            TextNode("This is text", TextType.BOLD),
            ]
        test = split_nodes_delimiter([TextNode("This is text", TextType.BOLD)], "**", TextType.BOLD)
        self.assertEqual(expected, test, "ERROR: Markdown to HTML conversion not working")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph
            
            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line
            
            - This is a list
            - with items
            """
        blocks = block.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here
    
    This is another paragraph with _italic_ text and `code` here
    
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()