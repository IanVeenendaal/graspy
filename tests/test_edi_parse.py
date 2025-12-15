import xml.etree.ElementTree as ET
from pathlib import Path

dir = Path(__file__).parent.parent / "tests"
file = "test.edi"
filename = dir / file

tree = ET.parse(filename)
root = tree.getroot()

ns = {"edi": "http://www.edi-forum.org"}


# Get Frequencies
freqs = (
    root.find(".//edi:Variable[@Class='Frequency']", ns)
    .find("edi:Component", ns)
    .find("edi:Value", ns)
    .text.split()
)
freqs = [float(freq) for freq in freqs]
print(f"Frequencies: {freqs}")

# Get Beamwidth Data
levels = (
    root.find(".//edi:Variable[@Class='BeamWidthLevels']", ns)
    .find("edi:Component", ns)
    .find("edi:Value", ns)
    .text.split()
)
levels = [float(lvl) for lvl in levels]
print(f"Beamwidth Levels: {levels}")


data = root.find("edi:Data", ns)
bw = data.find(".//edi:Variable[@Name='smooth_radiating_device_BeamWidth']", ns)
comp = bw.find("edi:Component", ns)
bw_value = comp.find("edi:Value", ns)
bw_values = bw_value.text.split()
bw_values = [float(val) for val in bw_values]
print(f"Beamwidth Values: {bw_values}")
