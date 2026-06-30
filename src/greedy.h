#include "graph_functions.h"


int solve_greedy(Graph g){
    int count = 0;
    while(!is_empty(&g)){
        // 1. Gaseste nodul cu grad maxim
        int max_degree = -1;
        int best_node = -1;

        for(int i = 0; i < g.n; i++){
            if(!g.active[i]) 
                continue;
            int degree = 0;
            for(int j = 0; j < g.n; j++){
                if(g.active[j] && g.adj[i][j]){
                    degree++;
                }
            }
            if(degree > max_degree){
                max_degree = degree;
                best_node = i;
            }
        }
        // 2. Adauga in solutie
        if(best_node != -1){
            count++;
            remove_node(&g, best_node);
        }
        else{
            break; 
        }
    }
    return count;
}