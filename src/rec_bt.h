#pragma once
#include "graph_functions.h"

// Optimized version: receives pointer to avoid copying the graph at each step
int solve_exact(Graph *g) { 
    // Base condition: if there are no more edges, we are done
    if (is_empty(g)) 
        return 0;

    // Find the first available edge (u, v)
    int u = -1, v = -1;

    for(int i = 0; i < g->n; i++){
        if(!g->active[i]) continue;
        
        for(int j = i + 1; j < g->n; j++){
            if(g->active[j] && g->adj[i][j]){
                u = i; 
                v = j;
                break;
            }
        }
        if(u != -1) break; 
    }

    // --- BRANCH 1: choose U ---

    // 1. Modify original graph (Backtracking: Do) - mark node as removed
    g->active[u] = false; 
    
    // 2. Recursive call
    int res1 = 1 + solve_exact(g);
    
    // 3. Restore graph (Backtracking: Undo) - put node back
    g->active[u] = true; 


    // --- BRANCH 2: choose V ---
    
    // 1. Modify graph
    g->active[v] = false;
    
    // 2. Recursive call
    int res2 = 1 + solve_exact(g);
    
    // 3. Restore graph
    g->active[v] = true;

    // Return minimum of the two branches
    return (res1 < res2) ? res1 : res2;
}