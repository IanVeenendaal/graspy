from pathlib import Path
from graspy.data.cut import read_cut_file, plot_cut_list

DIR = Path(
    r"C:\Users\Ian Veenendaal\OneDrive - Cardiff University\Projects\SOUK\models\Optics\US-SATs\GRASP\sat_model_cardiff\working"
)
FILE = "Horn_090_5p3.cut"
# FILE = "Horn_150_5p3.cut"


def main():
    file = DIR / FILE
    cuts = read_cut_file(file)
    plot_cut_list(cuts)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    main()
    plt.show()
