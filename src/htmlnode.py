# HTML
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag             # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value         # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children   # A list of HTMLNode objects representing the children of this node
        self.props = props         # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def __repr__(self):
        return f"TextNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

    def to_html(self):
        raise NotImplementedError("ERROR: Not Implemented")

    def props_to_html(self):
        if not self.props or self.props == {} or self.props is None:
            return ""
        conversion = ""
        for key, value in self.props.items():
            conversion += f" {key}=\"{value}\""
        return conversion


# Leaf (HTML)
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"TextNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        if not self.value or self.value == "" or self.value is None:
            raise ValueError("ERROR: No Value Attribute")
        if not self.tag or self.tag == "" or self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


# Parent HTML
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.children or self.children == "" or self.children is None:
            raise ValueError("ERROR: No Children Attribute")
        if not self.tag or self.tag == "" or self.tag is None:
            raise ValueError("ERROR: No Tag Attribute")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"