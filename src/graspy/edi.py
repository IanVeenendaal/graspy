import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd


def parse_edi_phase_centers(filename: Path):
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
    freqs = [float(freq) * 1e-9 for freq in freqs]

    # Get Beamwidth Levels
    levels = (
        root.find(".//edi:Variable[@Class='BeamWidthLevels']", ns)
        .find("edi:Component", ns)
        .find("edi:Value", ns)
        .text.split()
    )
    levels = [float(lvl) for lvl in levels]

    # Get Phi Planes
    phi = (
        root.find(".//edi:Variable[@Class='Phi']", ns)
        .find("edi:Component", ns)
        .find("edi:Value", ns)
        .text.split()
    )
    phi = [float(p) for p in phi]

    # Get Phase Center Data
    data = root.find("edi:Data", ns)
    bw = data.find(
        ".//edi:Variable[@Name='smooth_radiating_device_PhaseCenter']", ns
    )
    comp = bw.find("edi:Component", ns)
    bw_value = comp.find("edi:Value", ns)
    bw_values = bw_value.text.split()
    bw_values = [float(val) for val in bw_values]

    # Reshape bw_values
    n_levels = len(levels)
    n_freqs = len(freqs)
    n_planes = len(phi)
    bw_array = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            [freqs, phi], names=["Frequency (GHz)", "Phi (deg)"]
        ),
        columns=[f"{lvl} dB Phase Center" for lvl in levels],
    )
    for i in range(n_freqs):
        for j in range(n_levels):
            for k in range(n_planes):
                idx = i * n_levels * n_planes + j * n_planes + k
                bw_array.iat[i * n_planes + k, j] = bw_values[idx]

    return bw_array


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
    freqs = [float(freq) * 1e-9 for freq in freqs]

    # Get Beamwidth Levels
    levels = (
        root.find(".//edi:Variable[@Class='BeamWidthLevels']", ns)
        .find("edi:Component", ns)
        .find("edi:Value", ns)
        .text.split()
    )
    levels = [float(lvl) for lvl in levels]

    # Get Phi Planes
    phi = (
        root.find(".//edi:Variable[@Class='Phi']", ns)
        .find("edi:Component", ns)
        .find("edi:Value", ns)
        .text.split()
    )
    phi = [float(p) for p in phi]

    # Get Beamwidth Data
    data = root.find("edi:Data", ns)
    bw = data.find(
        ".//edi:Variable[@Name='smooth_radiating_device_BeamWidth']", ns
    )
    comp = bw.find("edi:Component", ns)
    bw_value = comp.find("edi:Value", ns)
    bw_values = bw_value.text.split()
    bw_values = [float(val) for val in bw_values]

    # Reshape bw_values
    n_levels = len(levels)
    n_freqs = len(freqs)
    n_planes = len(phi)
    bw_array = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            [freqs, phi], names=["Frequency (GHz)", "Phi (deg)"]
        ),
        columns=[f"BW Level {lvl} (dB)" for lvl in levels],
    )
    for i in range(n_freqs):
        for j in range(n_levels):
            for k in range(n_planes):
                idx = i * n_levels * n_planes + j * n_planes + k
                bw_array.iat[i * n_planes + k, j] = bw_values[idx]

    return bw_array


def parse_edi_crosspol(filename: Path):
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
    freqs = [float(freq) * 1e-9 for freq in freqs]

    # Get Cross-Pol Data
    cp = root.find(".//edi:Variable[@Class='LevelCxMax']", ns)
    comp = cp.find("edi:Component", ns)
    cp_value = comp.find("edi:Value", ns)
    cp_values = cp_value.text.split()
    cp_values = [float(val) for val in cp_values]

    # Reshape cp_values
    n_freqs = len(freqs)
    cp_array = pd.DataFrame(
        index=pd.Index(freqs, name="Frequency (GHz)"),
        columns=["Cross-Pol (dB)"],
    )
    for i in range(n_freqs):
        cp_array.iat[i, 0] = cp_values[i]

    return cp_array


def parse_edi_efficiency(filename: Path):
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
    freqs = [float(freq) * 1e-9 for freq in freqs]

    # Get Efficiency Data
    eff = (
        root.find(".//edi:Variable[@Class='Efficiency']", ns)
        .find("edi:Component", ns)
        .find("edi:Value", ns)
    )
    eff_values = [float(val) for val in eff.text.split()]

    # Create DataFrame
    eff_df = pd.DataFrame(
        data={"Efficiency": eff_values},
        index=pd.Index(freqs, name="Frequency (GHz)"),
    )
    return eff_df
