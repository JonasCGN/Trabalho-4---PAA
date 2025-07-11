import heapq
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import os

matplotlib.use('TkAgg')  # Força backend TkAgg para evitar problemas com Qt

def gerar_passos_prim(grafo, inicio=0):
    n = len(grafo)
    visitado = [False] * n
    min_heap = [(0, inicio, -1)]  # (peso, vértice, origem)
    agm = []
    passos = []
    custo_total = 0
    while min_heap:
        peso, u, origem = heapq.heappop(min_heap)
        if visitado[u]:
            continue
        visitado[u] = True
        custo_total += peso
        if origem != -1:
            agm.append((origem, u, peso))
        passos.append(list(agm))  # Salva o estado atual da AGM
        for v in range(n):
            if not visitado[v] and grafo[u][v] != 0:
                heapq.heappush(min_heap, (grafo[u][v], v, u))
    return passos, custo_total, agm

def salvar_grafo_agm(grafo, agm, path_salvar):
    """
    Gera uma imagem do grafo com a AGM destacada e salva no caminho especificado.
    Se a pasta não existir, ela será criada.
    - grafo: matriz de adjacência
    - agm: lista de tuplas (u, v, peso) da AGM
    - path_salvar: caminho do arquivo para salvar a imagem (ex: 'resultados/agm.png')
    """
    import matplotlib.pyplot as plt
    import networkx as nx

    # Cria a pasta se não existir
    pasta = os.path.dirname(path_salvar)
    if pasta and not os.path.exists(pasta):
        os.makedirs(pasta)

    G = nx.Graph()
    n = len(grafo)
    for i in range(n):
        for j in range(i+1, n):
            peso = grafo[i][j]
            if peso != 0:
                G.add_edge(i, j, weight=peso)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=12)
    agm_edges = [(u, v) for u, v, _ in agm]
    labels = nx.get_edge_attributes(G, 'weight')
    labels_sem_agm = {edge: w for edge, w in labels.items() if edge not in agm_edges and (edge[1], edge[0]) not in agm_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_sem_agm)
    if agm:
        nx.draw_networkx_edges(G, pos, edgelist=agm_edges, width=4, edge_color='red')
        for u, v, peso in agm:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
            plt.text(xm, ym + 0.07, str(peso), color='red', fontsize=14, fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, boxstyle='round,pad=0.1'))
    plt.title('Árvore Geradora Mínima (AGM) destacada')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path_salvar, bbox_inches='tight')
    plt.close()

def salvar_grafo_agm_pronto(grafo, path_salvar="resultados/agm_final.png"):
    """
    Exibe o grafo com a AGM destacada.
    - grafo: matriz de adjacência
    - agm: lista de tuplas (u, v, peso) da AGM
    """
    _, _, agm_final = gerar_passos_prim(grafo)
    salvar_grafo_agm(grafo, agm_final, path_salvar)
    print(f"Grafo com AGM salva em: {path_salvar}")

def prim_interativo_visual(grafo, inicio=0):
    import matplotlib.pyplot as plt
    import networkx as nx
    n = len(grafo)
    visitado = [False] * n
    min_heap = [(0, inicio, -1)]  # (peso, vértice, origem)
    agm = []
    heap_hist = []
    aresta_hist = []
    agm_hist = []
    passo = 0
    custo_total = 0
    # Executa Prim e salva o histórico de cada passo
    while min_heap:
        heap_hist.append(list(min_heap))
        peso, u, origem = heapq.heappop(min_heap)
        aresta_hist.append((peso, u, origem))
        if visitado[u]:
            agm_hist.append(list(agm))
            continue
        visitado[u] = True
        custo_total += peso
        if origem != -1:
            agm.append((origem, u, peso))
        agm_hist.append(list(agm))
        for v in range(n):
            if not visitado[v] and grafo[u][v] != 0:
                heapq.heappush(min_heap, (grafo[u][v], v, u))
    total = len(agm_hist)
    # Visualização interativa
    fig, ax = plt.subplots(figsize=(8,6))
    passo = [0]
    sair = [False]
    def desenhar_passo():
        ax.clear()
        G = nx.Graph()
        for i in range(n):
            for j in range(i+1, n):
                peso = grafo[i][j]
                if peso != 0:
                    G.add_edge(i, j, weight=peso)
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=12, ax=ax)
        agm_edges = [(u, v) for u, v, _ in agm_hist[passo[0]]] if agm_hist[passo[0]] else []
        labels = nx.get_edge_attributes(G, 'weight')
        labels_sem_agm = {edge: w for edge, w in labels.items() if edge not in agm_edges and (edge[1], edge[0]) not in agm_edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_sem_agm, ax=ax)
        if agm_hist[passo[0]]:
            nx.draw_networkx_edges(G, pos, edgelist=agm_edges, width=4, edge_color='red', ax=ax)
            for u, v, peso in agm_hist[passo[0]]:
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
                ax.text(xm, ym + 0.07, str(peso), color='red', fontsize=14, fontweight='bold', ha='center', va='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, boxstyle='round,pad=0.1'))
        # Mostra informações do passo
        info = f"Passo {passo[0]+1}/{total}\n"
        info += f"Heap: {heap_hist[passo[0]]}\n"
        peso, u, origem = aresta_hist[passo[0]]
        info += f"Aresta escolhida: peso={peso}, destino={u}, origem={origem if origem!=-1 else 'N/A'}\n"
        info += f"Arestas na AGM: {[ (u,v,p) for u,v,p in agm_hist[passo[0]] ]}"
        ax.set_title(info)
        fig.canvas.draw()
    def on_key(event):
        if event.key in ['right', 'd']:
            if passo[0] < total-1:
                passo[0] += 1
                desenhar_passo()
        elif event.key in ['left', 'a']:
            if passo[0] > 0:
                passo[0] -= 1
                desenhar_passo()
        elif event.key == 'q':
            sair[0] = True
            plt.close(fig)
    desenhar_passo()
    cid = fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()
    fig.canvas.mpl_disconnect(cid)
    if sair[0]:
        print("Execução interrompida pelo usuário.")
    print(f"Custo Total da AGM: {custo_total}")
    print("Arestas na AGM:")
    for u, v, peso in agm_hist[-1]:
        print(f"  {u} - {v} (peso {peso})")
    return custo_total, agm_hist[-1]

# Exemplo de uso
if __name__ == "__main__":
    grafo = [
        [0, 2, 0, 6, 0],
        [2, 0, 3, 8, 5],
        [0, 3, 0, 0, 7],
        [6, 8, 0, 0, 9],
        [0, 5, 7, 9, 0]
    ]
    # Gera os passos do algoritmo de Prim e exibe o grafo final
    # passos, custo_total, agm_final = gerar_passos_prim(grafo)
    # salvar_grafo_agm_pronto(grafo)
    
    prim_interativo_visual(grafo)