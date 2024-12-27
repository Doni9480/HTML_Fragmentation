from typing import Generator
from bs4 import BeautifulSoup, Tag
import argparse
import sys


class HTMLFragmenter:
    def __init__(self, max_len: int):
        self.max_len = max_len

    def split_html(self, html: str) -> Generator[str, None, None]:
        soup = BeautifulSoup(html, "html.parser")
        current_fragment = ""
        fragments = []
        open_tags = []

        def close_tags():
            for tag in reversed(open_tags):
                nonlocal current_fragment
                current_fragment += f"</{tag}>"

        def open_tags_again():
            for tag in open_tags:
                nonlocal current_fragment
                current_fragment += f"<{tag}>"

        def process_node(node):
            nonlocal current_fragment
            if isinstance(node, Tag):
                start_tag = f"<{node.name}{''.join([f' {k}="{v}"' for k, v in node.attrs.items()])}>"
                end_tag = f"</{node.name}>"

                if len(current_fragment) + len(start_tag) > self.max_len:
                    close_tags()
                    fragments.append(current_fragment)
                    current_fragment = ""
                    open_tags_again()

                current_fragment += start_tag
                open_tags.append(node.name)

                for child in node.contents:
                    process_node(child)

                open_tags.pop()

                if len(current_fragment) + len(end_tag) > self.max_len:
                    close_tags()
                    fragments.append(current_fragment)
                    current_fragment = ""
                    open_tags_again()

                current_fragment += end_tag
            else:
                if len(current_fragment) + len(str(node)) > self.max_len:
                    close_tags()
                    fragments.append(current_fragment)
                    current_fragment = ""
                    open_tags_again()

                current_fragment += str(node)

        for element in soup.contents:
            process_node(element)

        if current_fragment:
            fragments.append(current_fragment)

        return fragments


def split_message(source: str, max_len=4096) -> Generator[str, None, None]:
    fragmenter = HTMLFragmenter(max_len)
    fragments = fragmenter.split_html(source)
    for fragment in fragments:
        yield fragment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split an HTML file into fragments.")
    parser.add_argument(
        "--max-len", type=int, required=True, help="Maximum length of each fragment."
    )
    parser.add_argument("file", type=str, help="Path to the source HTML file.")
    args = parser.parse_args()

    max_len = args.max_len
    source_file = args.file

    if max_len < 1024:
        print("Error: Minimum fragment length must be at least 1024 characters.")
        sys.exit(1)

    try:
        with open(source_file, "r") as file:
            source_message = file.read()

            for i, fragment in enumerate(
                split_message(source_message, max_len), start=1
            ):
                print(f"fragment #{i}: {len(fragment)} chars")
                print(fragment)
                print("-" * 20)
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
