import pandas as pd
from collections import defaultdict
from pymatgen.core import Composition
from pymatgen.util.plotting import periodic_table_heatmap
import matplotlib.pyplot as plt

def main():
#    df = pd.read_csv("Data_1st.csv")
    df = pd.read_csv("Data_sorted_152.csv")

    num_occurrence = defaultdict(int)
    for i, row in df.iterrows():
        formula = row['formula']
        if not formula:
            continue
        comp = Composition(formula)

        for elem in comp.elements:
            num_occurrence[str(elem)] += 1

    # Remove Oxygen element(e.g., Oxygen)
    num_occurrence.pop("O", None)

    ax = periodic_table_heatmap(
        elemental_data=num_occurrence,
        cmap="YlGn",
        max_row=8,
        cbar_label="Number of occurrences",
        value_format="%4d",
        show_plot=False,
        pymatviz=False
    )

    ax.figure.savefig("element_occurrences_152.eps", dpi=300, bbox_inches="tight")
    plt.show()

if __name__ == "__main__":
    main()
