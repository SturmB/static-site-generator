from textnode import TextNode, TextType


def main() -> None:
    sample: TextNode = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(sample)

main()
