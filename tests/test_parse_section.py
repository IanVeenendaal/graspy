from pathlib import Path
from graspy.parse import find_section, replace_value_in_section

# Example usage
dir = Path(__file__).parent.parent / "tests"
filename = dir / "L1.tor"

with open(filename, "r") as file:
    content = file.read()

section_name = "x000"
section_content = find_section(content, section_name)
print(section_content)

new_value = 0.1e-2
new_content = replace_value_in_section(
    content, section_name, "value", str(new_value)
)

new_section_content = find_section(new_content, section_name)
print(new_section_content)

# Save the modified content to a new file
new_filename = dir / "L1_modified.tor"

with open(new_filename, "w") as file:
    file.write(new_content)
