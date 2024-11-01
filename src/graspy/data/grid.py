import pandas as pd


# Function to read GRD file
def read_grd_file(file_path):
    with open(file_path, "r") as file:
        # Read title
        version = file.readline().strip().split(":")[-1].strip()
        name = file.readline().strip()
        source_field_name = file.readline().strip().split(":")[-1].strip()
        frequency_range_name = file.readline().strip().split(":")[-1].strip()
        assert file.readline().strip() == "FREQUENCIES [GHz]:"
        frequency = file.readline().strip()

        # read until "++++"
        while "++++" not in file.readline().strip():
            pass

        # Read grid data
        data = []
        ktype = int(file.readline().strip())
        nset, icomp, ncomp, igrid = [int(x) for x in file.readline().split()]

        for i in range(nset):
            # center of the grid
            ix, iy = [int(x) for x in file.readline().split()]

        for i in range(nset):
            # grid limits
            xs, ys, xe, ye = [float(x) for x in file.readline().split()]
            nx, ny, klimit = [int(x) for x in file.readline().split()]

            for j in range(ny):
                if klimit == 1:
                    i_s, i_n = [int(x) for x in file.readline().split()]
                else:
                    i_s, i_n = 0, nx
                y = ys + (j) * (ye - ys) / (ny - 1)
                for k in range(i_n):
                    x = xs + (i_s + k) * (xe - xs) / (nx - 1)
                    line = [float(s) for s in file.readline().split()]
                    co = line[0] + 1j * line[1]
                    cx = line[2] + 1j * line[3]
                    data.append([x, y, co, cx])

        # convert to pandas dataframe
        df = pd.DataFrame(data, columns=["x", "y", "co", "cx"])
        return df
