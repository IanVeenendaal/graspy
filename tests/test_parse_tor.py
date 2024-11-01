from pathlib import Path
from graspy.parse import parse_tor

# Example usage
dir = Path(__file__).parent.parent / "tests"
filename = dir / "example.tor"
parsed_data = parse_tor(filename)
print(parsed_data)
