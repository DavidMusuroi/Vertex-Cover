import pandas as pd
import matplotlib.pyplot as plt

# Citim fisierul
df = pd.read_csv("../results/results.csv")

# Împărțim datele
dense = df.iloc[:15]
sparse = df.iloc[16:30]
bipartit = df.iloc[31:45]
random = df.iloc[46:60]

# Functie de desenare + salvare
def draw_and_save(data, title, filename):
    x = data["Nodes"]

    plt.figure()
    plt.plot(x, data["Time_Exact"], label="Backtracking")
    plt.plot(x, data["Time_Approx"], label="Approx")
    plt.plot(x, data["Time_Greedy"], label="Greedy")

    plt.xlabel("Number of nodes")
    plt.ylabel("Running time (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True)

    plt.ylim(0, 0.6)

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

# Grafic pentru dense
draw_and_save(dense, "Dense_1-10", "../results/Dense.png")

# Grafic pentru sparse
draw_and_save(sparse, "Sparse_11-20", "../results/Sparse.png")

# Grafic pentru bipartit
draw_and_save(sparse, "Bipartit_21-30", "../results/Bipartit.png")

# Grafic pentru random
draw_and_save(sparse, "Random_31-40", "../results/Random.png")

print("Graficele au fost salvate ca fisiere PNG.")
