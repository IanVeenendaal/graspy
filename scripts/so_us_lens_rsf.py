from graspy.helpers.asphere_to_rsf import Surface, Lens, asphere_to_rsf
from pathlib import Path
import pandas as pd

lensdatafile = Path(
    r"C:\Users\Ian Veenendaal\OneDrive - Cardiff University\Projects\SOUK\data\external\zemax\sous_optics_v28.csv"
)


def read_surface_data(lensdata: pd.DataFrame, row: int) -> Surface:
    radius = lensdata["Radius"][row]
    conic = lensdata["Conic"][row]
    even_asphere = [
        lensdata["Par 1"][row],
        lensdata["Par 2"][row],
        lensdata["Par 3"][row],
    ]
    return Surface(radius, conic, even_asphere)


def main():
    # Read in the lens data
    lensdata = pd.read_csv(lensdatafile, index_col=0)

    # create lens surfaces
    # Get index where Comment matches string
    l1_row = lensdata.index[lensdata["Comment"] == "Lens 1"].tolist()[0]
    l2_row = lensdata.index[lensdata["Comment"] == "Lens 2"].tolist()[0]
    l3_row = lensdata.index[lensdata["Comment"] == "Lens 3"].tolist()[0]
    stop_row = lensdata.index[lensdata["Comment"] == "Lyot"].tolist()[0]

    # Distance from stop to lens 1
    stop_to_lens1 = lensdata["Thickness"][stop_row:l1_row].sum()
    # Distance from stop to lens 2
    stop_to_lens2 = lensdata["Thickness"][stop_row:l2_row].sum()
    # Distance from stop to lens 3
    stop_to_lens3 = lensdata["Thickness"][stop_row:l3_row].sum()
    # Distance from stop to focal plane
    stop_to_focal_plane = lensdata["Thickness"][stop_row:].sum()

    print(
        f"Stop to lens 1: {stop_to_lens1}\nStop to lens 2: {stop_to_lens2}\nStop to lens 3: {stop_to_lens3}\nStop to focal plane: {stop_to_focal_plane}"
    )

    lens_rows = {
        "L1": [l1_row, l1_row + 1],
        "L2": [l2_row, l2_row + 1],
        "L3": [l3_row, l3_row + 1],
    }

    for i, (lens, rows) in enumerate(lens_rows.items()):
        ls1 = read_surface_data(lensdata, rows[0])
        ls2 = read_surface_data(lensdata, rows[1])
        lt = lensdata["Thickness"][rows[0]]
        lap = 22.5

        # Create RSF file
        lens = Lens(
            name=f"{i+1}", surface=[ls1, ls2], thickness=lt, aperture=lap
        )
        asphere_to_rsf(lens=lens, prefix="SOUS_", wavelength=1)


if __name__ == "__main__":
    main()
