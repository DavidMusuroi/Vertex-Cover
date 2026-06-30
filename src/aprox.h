#include "graph_functions.h"


int solve_approx(Graph g){
    int count = 0;
    while(!is_empty(&g)){
        // 1. Gaseste o muchie (u, v)
        int u = -1, v = -1;
        for(int i = 0; i < g.n && u == -1; i++){
            if(!g.active[i]) 
                continue;
            for(int j = i + 1; j < g.n; j++){
                if(g.active[j] && g.adj[i][j]){
                    u = i; 
                    v = j;
                    break;
                }
            }
        }
        // 2. Adauga AMBELE in solutie
        if(u != -1){
            count += 2;
            remove_node(&g, u);
            remove_node(&g, v);
        }
    }
    return count;
}