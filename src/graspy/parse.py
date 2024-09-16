import re
from pathlib import Path

from graspy.tor import struct, reference


def parse_tor(filename: Path):
    with open(filename, "r") as file:
        content = file.read()

    # remove content after //DO NOT MODIFY OBJECTS BELOW THIS LINE.
    content = content.split("//DO NOT MODIFY OBJECTS BELOW THIS LINE.")[0]

    # Regular expressions to match the blocks and their contents
    block_pattern = re.compile(r"(\w+)\s+(\w+)\s*\n\((.*?)\n\)", re.DOTALL)
    struct_pattern = re.compile(r"struct\((.*?)\)")
    ref_pattern = re.compile(r"ref\((.*?)\)")

    data = {}

    for match in block_pattern.finditer(content):
        block_name = match.group(1)
        block_type = match.group(2)
        block_content = match.group(3).strip()

        print(block_name, block_type, block_content)

        block_data = {}
        for line in block_content.split("\n"):
            line = line.strip()
            if not line:
                continue
            key, value = line.split(":", maxsplit=1)
            key = key.strip()
            value = value.strip()

            # Check if the value is a struct
            struct_match = struct_pattern.match(value)
            # Check if the value is a reference
            ref_match = ref_pattern.match(value)

            if struct_match:
                struct_content = struct_match.group(1)
                struct_data = {}
                for item in struct_content.split(","):
                    item_key, item_value = item.split(":", maxsplit=2)
                    struct_data[item_key.strip()] = item_value.strip()
                value = struct_data

            if ref_match:
                value = reference(value)

            block_data[key] = value

        data[block_name] = {"type": block_type, "data": block_data}

    return data
