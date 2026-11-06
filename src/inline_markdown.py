from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise SyntaxError("One or more delimiters are not closed")

        sections: list[str] = old_node.text.split(delimiter)
        print(sections)
        split_nodes: list[TextNode] = []
        for i in range(len(sections)):
            print(sections[i])
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
    
        new_nodes.extend(split_nodes)

    return new_nodes
