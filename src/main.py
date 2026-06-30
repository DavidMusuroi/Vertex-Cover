import subprocess
import random
import os
import csv
import time

# --- CONFIGURARE ---
C_SOURCE = "main.c"
# Detectare automata a executabilului in functie de OS
EXECUTABLE = "main.exe" if os.name == 'nt' else "./main"
OUTPUT_CSV = "../results/results.csv"

# Pragul peste care nu mai rulam algoritmul Exact (Backtracking)
# N=30 este limita rezonabila (aprox 1 miliard operatii). N=50 ar dura secole.
EXACT_ALGORITHM_LIMIT = 30 

def compile_c():
    """Compileaza codul C."""
    print(f"Compilare {C_SOURCE}...")
    cmd = ["gcc", C_SOURCE, "-o", "main", "-O2"]
    if os.name == 'nt':
        cmd = ["gcc", C_SOURCE, "-o", "main.exe", "-O2"]
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("Eroare la compilare! Verifica codul C.")
        exit(1)
    print("Compilare reusita.\n")

def generate_graph_str(n, edges):
    """Converteste lista de muchii in formatul acceptat de programul C."""
    input_str = f"{n} {len(edges)}\n"
    for u, v in edges:
        input_str += f"{u} {v}\n"
    return input_str

def get_bipartite_edges(n, density):
    """Genereaza muchii pentru un graf bipartit."""
    edges = []
    # Impartim nodurile in doua seturi: U (0..mid-1) si V (mid..n-1)
    mid = n // 2
    for u in range(mid):
        for v in range(mid, n):
            if random.random() < density:
                edges.append((u, v))
    return edges

def get_standard_edges(n, density):
    """Genereaza muchii pentru un graf general (Dense/Sparse/Random)."""
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                edges.append((i, j))
    return edges

def generate_test_case(n, category):
    """
    Returneaza string-ul de input pentru un graf bazat pe categorie.
    """
    edges = []
    
    if category == "Dense":
        # Probabilitate mare de muchie (0.7 - 0.9)
        edges = get_standard_edges(n, density=0.8)
        
    elif category == "Sparse":
        # Probabilitate mica (0.1 - 0.2)
        # Pentru N mare, reducem si mai mult densitatea sa nu fie prea greu I/O
        dens = 0.2 if n < 100 else 0.05
        edges = get_standard_edges(n, density=dens)
        
    elif category == "Random":
        # Probabilitate medie (0.5)
        edges = get_standard_edges(n, density=0.5)
        
    elif category == "Bipartit":
        # Graf bipartit cu densitate medie intre partitii
        edges = get_bipartite_edges(n, density=0.5)
        
    return generate_graph_str(n, edges)

def run_single_test(test_id, n, category):
    """Ruleaza executabilul C pentru un singur test."""
    
    # Generam datele
    input_data = generate_test_case(n, category)
    
    # Decidem daca rulam algoritmul Exact
    skip_exact = True if n > EXACT_ALGORITHM_LIMIT else False
    arg_skip = "1" if skip_exact else "0"
    
    # Rulam procesul
    try:
        process = subprocess.Popen(
            [EXECUTABLE, arg_skip],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_data)
        
        if process.returncode != 0:
            print(f"Eroare Runtime la {test_id}: {stderr}")
            return None
            
        # Parsam linia CSV returnata de C
        # Format C: N,TimeEx,TimeAp,TimeGr,SolEx,SolAp,SolGr
        line = stdout.strip()
        parts = line.split(',')
        
        # Ajustam outputul pentru Exact daca a fost sarit
        if skip_exact:
            # In C apare ca 0.000000 si -1, le facem N/A pentru raport
            parts[1] = "N/A" # Time_Exact
            parts[4] = "N/A" # Sol_Exact
            
        return [test_id, category] + parts

    except Exception as e:
        print(f"Exceptie Python la {test_id}: {e}")
        return None

def main():
    compile_c()
    
    # Configurare experiment
    sizes = [10, 20, 30, 50, 100, 200, 300, 400, 500, 600, 700, 800, 1000, 1100, 1200]
    runs_per_case = 1
    categories = ["Dense", "Sparse", "Bipartit", "Random"]
    
    results = []
    
    print(f"{'TestID':<15} {'Categ':<10} {'Nodes':<6} {'Status'}")
    print("-" * 50)
    
    test_counter = 1
    
    for category in categories:
        for n in sizes:
            for i in range(runs_per_case):
                test_id = f"T{test_counter:02d}_{category}_{n}"
                
                print(f"{test_id:<15} {category:<10} {n:<6} ...", end="", flush=True)
                
                row = run_single_test(test_id, n, category)
                
                if row:
                    results.append(row)
                    print(" Done")
                else:
                    print(" Failed")
                
                test_counter += 1

    # Salvare in CSV
    header = ["TestID", "Category", "Nodes", "Time_Exact", "Time_Approx", "Time_Greedy", "Sol_Exact", "Sol_Approx", "Sol_Greedy"]
    
    try:
        with open(OUTPUT_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(results)
        print(f"\n Rezultate salvate cu succes in '{OUTPUT_CSV}'")
        print(f"Total teste generate: {len(results)}")
    except IOError as e:
        print(f"\n Eroare la scrierea fisierului CSV: {e}")

if __name__ == "__main__":
    main()