#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include "graph_functions.h"
#include "greedy.h"
#include "aprox.h"
#include "rec_bt.h"

Graph g;

int main(int argc, char *argv[]) {
    read_graph(&g);

    // Command-line argument decides whether we also run Exact
    // 0 = run everything, 1 = only Approx and Greedy (for large graphs)
    int skip_exact = 0;
    double time_exact = 0.0;
    int res_exact = -1;

    if(argc > 1)
        skip_exact = atoi(argv[1]);

    // Exact measurement
    if (!skip_exact) {
        clock_t start = clock();
        res_exact = solve_exact(&g);
        clock_t end = clock();
        time_exact = (double)(end - start) / CLOCKS_PER_SEC;
    }

    // Approx measurement
    clock_t start_ap = clock();
    int res_approx = solve_approx(g);
    clock_t end_ap = clock();
    double time_approx = (double)(end_ap - start_ap) / CLOCKS_PER_SEC;

    // Greedy measurement
    clock_t start_gr = clock();
    int res_greedy = solve_greedy(g);
    clock_t end_gr = clock();
    double time_greedy = (double)(end_gr - start_gr) / CLOCKS_PER_SEC;

    // Output format: N, TimeEx, TimeAp, TimeGr, SolEx, SolAp, SolGr
    // Using CSV format for easy parsing
    printf("%d,%.6f,%.6f,%.6f,%d,%d,%d\n", 
           g.n, time_exact, time_approx, time_greedy, res_exact, res_approx, res_greedy);

    return 0;
}