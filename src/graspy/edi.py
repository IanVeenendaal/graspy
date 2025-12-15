import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd


def parse_edi_beamwidths(filename: Path):
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

    # Get Beamwidth Data
    levels = (
        root.find(".//edi:Variable[@Class='BeamWidthLevels']", ns)
        .find("edi:Component", ns)
        .find("edi:Value", ns)
        .text.split()
    )
    levels = [float(lvl) for lvl in levels]

    data = root.find("edi:Data", ns)
    bw = data.find(
        ".//edi:Variable[@Name='smooth_radiating_device_BeamWidth']", ns
    )
    comp = bw.find("edi:Component", ns)
    bw_value = comp.find("edi:Value", ns)
    bw_values = bw_value.text.split()
    bw_values = [float(val) for val in bw_values]

    # Reshape bw_values into a 2D list
    n_levels = len(levels)
    n_freqs = len(freqs)
    bw_matrix = []
    for i in range(n_levels):
        start_idx = i * n_freqs
        end_idx = start_idx + n_freqs
        bw_matrix.append(bw_values[start_idx:end_idx])
    bw_df = pd.DataFrame(bw_matrix, index=levels, columns=freqs)
    bw_df.index.name = "Beamwidth Levels (deg)"
    bw_df.columns.name = "Frequencies (GHz)"
    return bw_df
