#pragma once
#include "graph_functions.h"

// Varianta optimizata: Primeste pointer (*g) pentru a NU copia graful la fiecare pas
int solve_exact(Graph *g) { 
    // Conditia de oprire: daca nu mai sunt muchii, am terminat
    if (is_empty(g)) 
        return 0;

    // Gaseste prima muchie disponibila (u, v)
    int u = -1, v = -1;

    // Cautam muchia
    for(int i = 0; i < g->n; i++){
        if(!g->active[i]) continue;
        
        for(int j = i + 1; j < g->n; j++){
            if(g->active[j] && g->adj[i][j]){
                u = i; 
                v = j;
                break; // Iesim din bucla interioara
            }
        }
        // Verificare pentru a iesi si din bucla exterioara
        if(u != -1) break; 
    }

    // --- RAMURA 1: Il alegem pe U ---
    // 1. Modificam graful original (Backtracking: Do) - marcam nodul ca sters
    g->active[u] = false; 
    
    // 2. Apelam recursiv
    int res1 = 1 + solve_exact(g);
    
    // 3. Refacem graful (Backtracking: Undo) - punem nodul la loc
    g->active[u] = true; 


    // --- RAMURA 2: Il alegem pe V ---
    // 1. Modificam
    g->active[v] = false;
    
    // 2. Apelam recursiv
    int res2 = 1 + solve_exact(g);
    
    // 3. Refacem
    g->active[v] = true;

    // Returnam minimul dintre cele doua ramuri
    return (res1 < res2) ? res1 : res2;
}