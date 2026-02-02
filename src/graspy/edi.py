import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd

ns = {"edi": "http://www.edi-forum.org"}


def _get_data_variable_name(root: ET.Element, name_contains: str) -> str:
    variables = root.findall(f".//edi:Data/edi:Variable", ns)
    for var in variables:
        var_name = var.attrib["Name"]
        if name_contains.lower() in var_name.lower():
            return var_name
    raise ValueError(f"Variable containing '{name_contains}' not found.")


def _get_variable_data(root: ET.Element, class_name: str) -> list:
    # Find data in the root class first
    value = root.find(
        f".//edi:Variable[@Class='{class_name}']/edi:Component/edi:Value", ns
    )

    # If not found, look in the Data section
    if value is None:
        variable_name = _get_data_variable_name(root, class_name)
        if variable_name is None:
            raise ValueError(
                f"Variable with class name '{class_name}' not found."
            )

        value = root.find(
            f".//edi:Data/edi:Variable[@Name='{variable_name}']/edi:Component/edi:Value",
            ns,
        )
    if value is not None:
        return value.text.split()


def parse_edi_phase_centers(filename: Path):
    tree = ET.parse(filename)
    root = tree.getroot()

    # Get Frequencies
    freqs = get_frequencies_from_edi(filename)

    # Get Beamwidth Levels
    levels = _get_variable_data(root, "BeamWidthLevels")
    levels = [float(lvl) for lvl in levels]

    # Get Phi Planes
    phi = _get_variable_data(root, "Phi")
    phi = [float(p) for p in phi]

    # Get Phase Center Data
    pc_data = _get_variable_data(root, "PhaseCenter")
    pc_values = [float(val) for val in pc_data]

    # Reshape pc_values
    n_levels = len(levels)
    n_freqs = len(freqs)
    n_planes = len(phi)
    pc_array = pd.DataFrame(
        index=pd.MultiIndex.from_product(
            [freqs, phi], names=["Frequency (GHz)", "Phi (deg)"]
        ),
        columns=[f"{lvl} dB Phase Center" for lvl in levels],
    )
    for i in range(n_freqs):
        for j in range(n_levels):
            for k in range(n_planes):
                idx = i * n_levels * n_planes + j * n_planes + k
                pc_array.iat[i * n_planes + k, j] = pc_values[idx]

    return pc_array


def parse_edi_beamwidths(filename: Path):
    tree = ET.parse(filename)
    root = tree.getroot()

    # Get Frequencies
    freqs = get_frequencies_from_edi(filename)

    # Get Beamwidth Levels
    levels = _get_variable_data(root, "BeamWidthLevels")
    levels = [float(lvl) for lvl in levels]

    # Get Phi Planes
    phi = _get_variable_data(root, "Phi")
    phi = [float(p) for p in phi]

    # Get Beamwidth Data
    bw_values = _get_variable_data(root, "BeamWidth")
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

    # Get Frequencies
    freqs = get_frequencies_from_edi(filename)

    # Get Cross-Pol Data
    cp_values = _get_variable_data(root, "LevelCxMax")
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

    # Get Frequencies
    freqs = get_frequencies_from_edi(filename)

    # Get Efficiency Data
    eff = _get_variable_data(root, "Efficiency")
    eff_values = [float(val) for val in eff]

    # Create DataFrame
    eff_df = pd.DataFrame(
        data={"Efficiency": eff_values},
        index=pd.Index(freqs, name="Frequency (GHz)"),
    )
    return eff_df


def get_frequencies_from_edi(filename: Path):
    tree = ET.parse(filename)
    root = tree.getroot()

    freqs = _get_variable_data(root, "Frequency")
    freqs = [float(freq) * 1e-9 for freq in freqs]
    return freqs
