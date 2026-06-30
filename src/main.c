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

    // Argumentul din linia de comanda decide daca rulam si Exact
    // 0 = Ruleaza tot, 1 = Doar Approx si Greedy (pt grafuri mari)
    int skip_exact = 0;
    double time_exact = 0.0;
    int res_exact = -1;

    if(argc > 1)
        skip_exact = atoi(argv[1]);

    // Masurare Exact
    if (!skip_exact) {
        clock_t start = clock();
        res_exact = solve_exact(&g);
        clock_t end = clock();
        time_exact = (double)(end - start) / CLOCKS_PER_SEC;
    }

    // Masurare Approx
    clock_t start_ap = clock();
    int res_approx = solve_approx(g);
    clock_t end_ap = clock();
    double time_approx = (double)(end_ap - start_ap) / CLOCKS_PER_SEC;

    // Masurare Greedy
    clock_t start_gr = clock();
    int res_greedy = solve_greedy(g);
    clock_t end_gr = clock();
    double time_greedy = (double)(end_gr - start_gr) / CLOCKS_PER_SEC;

    // Output format: N, TimeEx, TimeAp, TimeGr, SolEx, SolAp, SolGr
    // Folosim CSV format pentru parsing usor
    printf("%d,%.6f,%.6f,%.6f,%d,%d,%d\n", 
    g.n, time_exact, time_approx, time_greedy, res_exact, res_approx, res_greedy);

    return 0;
}