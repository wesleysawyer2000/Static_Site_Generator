import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversions import *


class TestHTMLNode(unittest.TestCase):

    # HTML Tests
    def test_isEq(self):
        node1 = HTMLNode("p", "This is a node",)
        node2 = HTMLNode("p", "This is a node", )
        self.assertEqual(node1, node2, "FAIL: Nodes are NOT equal")

    def test_isNone(self):
        node1 = HTMLNode()
        self.assertIsNone(node1.tag, "FAIL: Tag attribute is NOT None")
        self.assertIsNone(node1.value, "FAIL: Tag attribute is NOT None")
        self.assertIsNone(node1.children, "FAIL: Tag attribute is NOT None")
        self.assertIsNone(node1.props, "FAIL: Tag attribute is NOT None")

    def test_children(self):
        node1 = HTMLNode("p", "This is a node",)
        node2 = HTMLNode("p", "This is a node", )
        node3 = HTMLNode("p", "This is a node", [node1, node2])
        self.assertIn(node1, node3.children, "FAIL: Children nodes NOT attached")

    def test_propsToHTML(self):
        node1 = HTMLNode("p", "This is a node", [], {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node1.props_to_html(), expected, "FAIL: Nodes are NOT equal")


    # Leaf Tests
    def test_leaf_subclass(self):
        #node1 = HTMLNode("p", "This is a node",)
        node1 = LeafNode("p", "This is a node",)
        self.assertIsInstance(node1, HTMLNode, "FAIL: LeafNode is NOT a subclass of HTMLNode")

    def test_leaf_toHTML(self):
        node1 = LeafNode("p", "Hello, world!", {
            "href": "https://www.google.com",
        })
        self.assertEqual(node1.to_html(), "<p href=\"https://www.google.com\">Hello, world!</p>")

    def test_leaf_children(self):
        node1 = LeafNode("p", "Hello, world!", {
            "href": "https://www.google.com",
        })
        self.assertIsNone(node1.children, "FAIL: LeafNode children attribute is NOT None")


    # Parent Tests
    def test_parent_toHTMLwithChildren(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_toHTMLwithGrandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_toHTMLwithMultipleChildrenGrandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild")
        grandchild_node3 = LeafNode("b", "grandchild")
        grandchild_node4 = LeafNode("b", "grandchild")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node3, grandchild_node4])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b></span><span><b>grandchild</b><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()