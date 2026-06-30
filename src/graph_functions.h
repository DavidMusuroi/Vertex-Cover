// Functie pentru citirea grafului
#pragma once
#include <stdio.h>
#include <stdbool.h>
#define max_nodes 1200 // Limita maximă de noduri (suficient pentru testele tale)

typedef struct {
    int adj[max_nodes][max_nodes]; // Matrice de adiacenta
    int n;                 // Numar noduri
    bool active[max_nodes];    // Daca nodul mai exista in graf
} Graph;

void read_graph(Graph *g) {
    int m, u, v;
    scanf("%d %d", &g->n, &m);
    
    // Initializare
    for(int i = 0; i < g->n; i++){
        g->active[i] = true;
        for(int j = 0; j < g->n; j++)
            g->adj[i][j] = 0;
    }

    for(int i = 0; i < m; i++){
        scanf("%d %d", &u, &v);
        if(u < g->n && v < g->n){
            g->adj[u][v] = 1;
            g->adj[v][u] = 1;
        }
    }
}

// Helper: Verifica daca graful mai are muchii
bool is_empty(Graph *g){
    for(int i = 0; i < g->n; i++){
        if (!g->active[i]) 
            continue;
        for(int j = i + 1; j < g->n; j++){
            if (g->active[j] && g->adj[i][j])
                return false;
        }
    }
    return true;
}

// Helper: Sterge un nod (il marcheaza inactiv)
void remove_node(Graph *g, int node) {
    g->active[node] = false;
}