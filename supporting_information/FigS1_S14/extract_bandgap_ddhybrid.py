import pandas as pd
from tqdm import tqdm
from get_db import get_database

def extract_diagonal_masses(p_tensor):
    try:
        m11 = p_tensor[0][0]
        m22 = p_tensor[1][1]
        m33 = p_tensor[2][2]
        return m11, m22, m33
    except Exception:
        return None, None, None

def main():
    # Load original CSV file with 'formula' and 'O-2p'
    df_input = pd.read_csv("data_sorted_845.csv")

    # Connect to MongoDB using your pacman.json
    db = get_database("../pacman.json")
    effmass_coll = db["effective_mass_dd_hybrid"]
    bandgap_coll = db["band_dd_hybrid"]

    # Prepare new columns
    hole_mass_11_list = []
    hole_mass_22_list = []
    hole_mass_33_list = []
    bandgap_list = []
    not_found = []

    for formula in tqdm(df_input["formula"]):
        m11 = m22 = m33 = bandgap = None

        # Get effective mass
        eff_doc = effmass_coll.find_one({"formula": formula})
        if eff_doc:
            try:
                p_tensor = eff_doc["effective_mass"]["p"][0]
                m11, m22, m33 = extract_diagonal_masses(p_tensor)
            except Exception as e:
                not_found.append((formula, f"Eff. mass parse error: {e}"))
        else:
            not_found.append((formula, "Eff. mass not found"))

        # Get bandgap
        band_doc = bandgap_coll.find_one({"formula": formula})
        if band_doc:
            bandgap = band_doc.get("band_gap")
        else:
            not_found.append((formula, "Bandgap not found"))

        # Store values
        hole_mass_11_list.append(m11)
        hole_mass_22_list.append(m22)
        hole_mass_33_list.append(m33)
        bandgap_list.append(bandgap)

    # Add new columns to the original DataFrame
    df_input["hole_mass_11"] = hole_mass_11_list
    df_input["hole_mass_22"] = hole_mass_22_list
    df_input["hole_mass_33"] = hole_mass_33_list
    df_input["bandgap"] = bandgap_list

    # Save final DataFrame
    df_input.to_csv("data_sorted_845_with_mass_bandgap.csv", index=False)
    print("Saved: data_845_gap_mass.csv")

    # Save log of missing data
    with open("missing_entries.log", "w") as f:
        for formula, reason in not_found:
            f.write(f"{formula}: {reason}\n")
    print("Saved: missing_entries.log")

if __name__ == "__main__":
    main()
