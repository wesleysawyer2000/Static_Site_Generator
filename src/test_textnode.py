import unittest
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_isEq(self):
        node1 = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertEqual(node1, node2, "FAIL: Nodes are NOT equal")

    def test_notEq(self):
        node1 = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.ITALIC)
        self.assertNotEqual(node1, node2, "FAIL: Nodes are equal")

    def test_urlIsNone(self):
        node1 = TextNode("This is a node", TextType.LINK)
        self.assertIsNone(node1.url, "FAIL: Node URL is NOT None")

    def test_urlNotNone(self):
        node2 = TextNode("This is a node", TextType.LINK, "https://www.boot.dev")
        self.assertIsNotNone(node2.url, "FAIL: Node URL is None")



if __name__ == "__main__":
    unittest.main()