import re
from pathlib import Path

from graspy.tor import struct, reference, sequence


def parse_tor(filename: Path):
    with open(filename, "r") as file:
        content = file.read()

    # remove content after //DO NOT MODIFY OBJECTS BELOW THIS LINE.
    content = content.split("//DO NOT MODIFY OBJECTS BELOW THIS LINE.")[0]

    # Regular expressions to match the blocks and their contents
    block_pattern = re.compile(r"(\w+)\s+(\w+)\s*\n\((.*?)\n\)", re.DOTALL)
    struct_pattern = re.compile(r"struct\((.*?)\)")
    ref_pattern = re.compile(r"ref\((.*?)\)")
    seq_pattern = re.compile(r"sequence\((.*?)\)")
    unit_pattern = re.compile(r"(.+)\s+(\w+)")

    data = {}

    for match in block_pattern.finditer(content):
        block_name = match.group(1)
        block_type = match.group(2)
        block_content = match.group(3).strip()

        print(block_name, block_type, block_content)

        block_data = {}
        for line in block_content.split("\n"):
            # remove trailing comma if present
            line = line.strip()
            if line.endswith(","):
                line = line[:-1]
            if not line:
                continue
            key, value = line.split(":", maxsplit=1)
            key = key.strip()
            value = value.strip()

            # Check if the value is a struct
            struct_match = struct_pattern.match(value)
            # Check if the value is a reference
            ref_match = ref_pattern.match(value)
            # Check if the value is a sequence
            sequence_match = seq_pattern.match(value)
            # check if the value has units
            unit_match = unit_pattern.match(value)

            if struct_match:
                value = convert_struct(struct_match.group(1))
            elif ref_match:
                value = convert_ref(ref_match.group(1))
            elif sequence_match:
                value = convert_sequence(sequence_match.group(1))
            elif unit_match:
                value = float(unit_match.group(1))
                unit = unit_match.group(2)
                value = (value, unit)
            else:
                try:
                    value = float(value)
                except ValueError:
                    pass

            block_data[key] = value

        data[block_name] = {"type": block_type, "data": block_data}

    return data


def convert_struct(struct_str: str) -> struct:
    """Converts string to GRASP struct object.

    Args:
        obj (str): String representation of a struct object.

    Returns:
        struct: GRASP struct object.
    """

    struct_data = {}
    for item in struct_str.split(","):
        item_key, item_value = item.split(":", maxsplit=2)
        struct_data[item_key.strip()] = item_value.strip()

    # If struct has units, split the value into value and units
    units = {}
    for key, value in struct_data.items():
        if " " in value:
            value_split = value.split(" ")
            struct_data[key] = value_split[0]
            units[key] = value_split[1]

    # Try convert values to float
    for key, value in struct_data.items():
        try:
            struct_data[key] = float(value)
        except ValueError:
            pass

    return struct(struct_data, units=units)


def convert_ref(ref_str: str) -> reference:
    """Converts string to GRASP reference object.

    Args:
        obj (str): String representation of a reference object.

    Returns:
        reference: GRASP reference object.
    """

    return reference(ref_str)


def convert_sequence(sequence_str: str) -> sequence:
    """Converts string to GRASP sequence object.

    Args:
        obj (str): String representation of a sequence object.

    Returns:
        sequence: GRASP sequence object.
    """

    sequence_list = {}
    for item in sequence_str.split(","):
        sequence_list.append(item.strip())

    # Check if the sequence has units
    units = []
    for i, item in enumerate(sequence_list):
        if " " in item:
            item_split = item.split(" ", maxsplit=1)
            sequence_list[i] = item_split[0]
            units.append(item_split[1])

    # Try convert values to float
    for i, item in enumerate(sequence_list):
        try:
            sequence_list[i] = float(item)
        except ValueError:
            pass

    # All units should be the same in a sequence
    if len(set(units)) > 1:
        raise ValueError("All units in a sequence should be the same.")

    # If units are present, create a sequence object with units
    if units:
        return sequence(sequence_list, units=units)

    return sequence(sequence_list)
