import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from matplotlib import pyplot as plt


@dataclass
class Cut:
    title: str
    v_ini: float
    v_inc: float
    v_num: int
    const: float
    icomp: int
    icut: int
    ncomp: int
    data: pd.DataFrame


def read_cut_file(file_path: Path) -> list[Cut]:
    cuts = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    # find lines with title
    title = lines[0].strip()
    title_lines = [i for i, line in enumerate(lines) if title in line]
    spacing = title_lines[1] - title_lines[0]
    assert all(
        title_lines[i + 1] - title_lines[i] == spacing
        for i in range(len(title_lines) - 1)
    )

    for i in range(len(title_lines)):
        data = lines[title_lines[i] + 1 : title_lines[i] + spacing]
        params = data[0].split()
        v_ini = float(params[0])
        v_inc = float(params[1])
        v_num = int(params[2])
        const = float(params[3])
        icomp = int(params[4])
        icut = int(params[5])
        ncomp = int(params[6])
        if ncomp == 2:
            co = []
            cx = []
            for d in data[1:]:
                line = d.split()
                co.append(float(line[0]) + 1j * float(line[1]))
                cx.append(float(line[2]) + 1j * float(line[3]))

            df = pd.DataFrame({"co": co, "cx": cx})
            df["x"] = df.index * v_inc + v_ini
        cut = Cut(
            title,
            v_ini,
            v_inc,
            v_num,
            const,
            icomp,
            icut,
            ncomp,
            df,
        )
        cuts.append(cut)

    return cuts


def plot_cut(cut: Cut, ax=None):
    ax.plot(cut.data["x"], cut.data["co"].values.real, label="co real")
    ax.plot(cut.data["x"], cut.data["co"].values.imag, label="co imag")
    ax.plot(cut.data["x"], cut.data["cx"].values.real, label="cx real")
    ax.plot(cut.data["x"], cut.data["cx"].values.imag, label="cx imag")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("Field")
    ax.set(yscale="log")
    ax.set_title(cut.const)


def plot_cut_list(cuts: list[Cut]):
    fig, ax = plt.subplots(ncols=2, nrows=len(cuts) // 2, figsize=(12, 12))
    for i, cut in enumerate(cuts):
        plot_cut(cut, ax=ax[i // 2, i % 2])
