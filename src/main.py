import subprocess
import random
import os
import csv
import time

# --- CONFIGURATION ---
C_SOURCE = "main.c"
# Automatic detection of executable depending on OS
EXECUTABLE = "main.exe" if os.name == 'nt' else "./main"
OUTPUT_CSV = "../results/results.csv"

# Threshold above which we do not run the Exact (Backtracking) algorithm
# N=30 is a reasonable limit (approx. 1 billion operations). N=50 would take ages.
EXACT_ALGORITHM_LIMIT = 30 

def compile_c():
    """Compiles the C code."""
    print(f"Compiling {C_SOURCE}...")
    cmd = ["gcc", C_SOURCE, "-o", "main", "-O2"]
    if os.name == 'nt':
        cmd = ["gcc", C_SOURCE, "-o", "main.exe", "-O2"]
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("Compilation error! Check C code.")
        exit(1)
    print("Compilation successful.\n")

def generate_graph_str(n, edges):
    """Converts edge list into the format expected by the C program."""
    input_str = f"{n} {len(edges)}\n"
    for u, v in edges:
        input_str += f"{u} {v}\n"
    return input_str

def get_bipartite_edges(n, density):
    """Generates edges for a bipartite graph."""
    edges = []
    # Split nodes into two sets: U (0...mid-1) and V (mid...n-1)
    mid = n // 2
    for u in range(mid):
        for v in range(mid, n):
            if random.random() < density:
                edges.append((u, v))
    return edges

def get_standard_edges(n, density):
    """Generates edges for a general graph (Dense/Sparse/Random)."""
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < density:
                edges.append((i, j))
    return edges

def generate_test_case(n, category):
    """
    Returns the input string for a graph based on category.
    """
    edges = []
    
    if category == "Dense":
        # High probability of edge (0.7 to 0.9)
        edges = get_standard_edges(n, density=0.8)
        
    elif category == "Sparse":
        # Low probability (0.1 - 0.2)
        # For large N, reduce density further to avoid heavy I/O
        dens = 0.2 if n < 100 else 0.05
        edges = get_standard_edges(n, density=dens)
        
    elif category == "Random":
        # Medium probability (0.5)
        edges = get_standard_edges(n, density=0.5)
        
    elif category == "Bipartite":
        # Bipartite graph with medium inter-partition density
        edges = get_bipartite_edges(n, density=0.5)
        
    return generate_graph_str(n, edges)

def run_single_test(test_id, n, category):
    """Runs the C executable for a single test."""
    
    # Generate input data
    input_data = generate_test_case(n, category)
    
    # Decide whether to run Exact algorithm
    skip_exact = True if n > EXACT_ALGORITHM_LIMIT else False
    arg_skip = "1" if skip_exact else "0"
    
    # Run process
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
            print(f"Runtime error at {test_id}: {stderr}")
            return None
            
        # Parse CSV line returned by C program
        # C format: N,TimeEx,TimeAp,TimeGr,SolEx,SolAp,SolGr
        line = stdout.strip()
        parts = line.split(',')
        
        # Adjust output for Exact if it was skipped
        if skip_exact:
            # In C it appears as 0.000000 and -1, convert to N/A for reporting
            parts[1] = "N/A"  # Time_Exact
            parts[4] = "N/A"  # Sol_Exact
            
        return [test_id, category] + parts

    except Exception as e:
        print(f"Python exception at {test_id}: {e}")
        return None

def main():
    compile_c()
    
    # Experiment configuration
    sizes = [10, 20, 30, 50, 100, 200, 300, 400, 500, 600, 700, 800, 1000, 1100, 1200]
    runs_per_case = 1
    categories = ["Dense", "Sparse", "Bipartite", "Random"]
    
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

    # Save to CSV
    header = ["TestID", "Category", "Nodes", "Time_Exact", "Time_Approx", "Time_Greedy", "Sol_Exact", "Sol_Approx", "Sol_Greedy"]
    
    try:
        with open(OUTPUT_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(results)
        print(f"\n Results successfully saved to '{OUTPUT_CSV}'")
        print(f"Total tests generated: {len(results)}")
    except IOError as e:
        print(f"\n Error writing CSV file: {e}")

if __name__ == "__main__":
    main()