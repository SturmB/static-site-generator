import re

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
        split_nodes: list[TextNode] = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
    
        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        working_text: str = old_node.text
        images: list[tuple[str, str]] = extract_markdown_images(working_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            surrounding_text: list[str] = working_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(surrounding_text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if surrounding_text[0] != "":
                new_nodes.append(TextNode(surrounding_text[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            working_text = surrounding_text[1]
        if working_text != "":
            new_nodes.append(TextNode(working_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        working_text: str = old_node.text
        links: list[tuple[str, str]] = extract_markdown_links(working_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            surrounding_text: list[str] = working_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(surrounding_text) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if surrounding_text[0] != "":
                new_nodes.append(TextNode(surrounding_text[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            working_text = surrounding_text[1]
        if working_text != "":
            new_nodes.append(TextNode(working_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
