import heapq

def prim(grafo, inicio=0):
    n = len(grafo)
    visitado = [False] * n
    min_heap = [(0, inicio)]  # (peso, vértice)
    custo_total = 0
    agm = []

    while min_heap:
        peso, u = heapq.heappop(min_heap)
        if visitado[u]:
            continue
        visitado[u] = True
        custo_total += peso

        for v in range(n):
            if not visitado[v] and grafo[u][v] != 0:
                heapq.heappush(min_heap, (grafo[u][v], v))
                agm.append((u, v, grafo[u][v]))

    return custo_total, agm

if __name__ == "__main__":
    
    grafo = [
        [0, 2, 0, 6, 0],
        [2, 0, 3, 8, 5],
        [0, 3, 0, 0, 7],
        [6, 8, 0, 0, 9],
        [0, 5, 7, 9, 0]
    ]
    
    custo, arvore = prim(grafo)

    print("Custo Total:", custo)
    print("Arestas na AGM:")
    for u, v, peso in arvore:
        print(f"{u} - {v} (peso {peso})")
