import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch
import argparse


# Génère un graphe orienté acyclique (DAG) aléatoire avec n sommets et une probabilité p
def generate_gnp_dag(n, p):
    """
    Génère un DAG aléatoire avec une probabilité p pour chaque arête (i -> j) avec i < j.
    Cela garantit l'absence de cycles.
    """
    matrice = [[0 for _ in range(n)] for _ in range(n)]  # matrice d'adjacence vide
    for i in range(n):
        for j in range(i + 1, n):  # pour garder le graphe acyclique, on ajoute uniquement i → j avec i < j
            if random.random() < p:
                matrice[i][j] = 1
    return matrice


# Génère les tâches et leurs dépendances à partir du DAG
def generate_tasks_and_precedences(n, p):
    matrix = generate_gnp_dag(n, p)

    # Construction directe des dépendances (prédécesseurs)
    precedences = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                precedences[j].append(i)

    # Génère un WCET (Worst Case Execution Time) aléatoire pour chaque tâche entre 1 et 10
    tasks = {i: random.randint(1, 10) for i in range(n)}

    return tasks, precedences


# Reconstruit les successeurs à partir des précédences (utile pour les calculs de rang)
def build_successors(precedences):
    successors = {}
    for task, preds in precedences.items():
        for p in preds:
            if p not in successors:
                successors[p] = []
            successors[p].append(task)
    return successors


# Calcule le "rank up" des tâches selon l'algorithme HEFT
def compute_ranks(tasks, precedences):
    successors = build_successors(precedences)
    ranks = {}

    def dfs(task):
        # Si le rang est déjà calculé, on le retourne
        if task in ranks:
            return ranks[task]
        succs = successors.get(task, [])
        # Rank = durée de la tâche + maximum des rangs de ses successeurs
        rank = tasks[task] + max((dfs(s) for s in succs), default=0)
        ranks[task] = rank
        return rank

    # On calcule le rang de toutes les tâches
    for task in tasks:
        dfs(task)

    return ranks


# Planifie les tâches selon l'algorithme HEFT
def heft_scheduler(tasks, precedences, nb_machines):
    ranks = compute_ranks(tasks, precedences)
    # Trie les tâches par rang décroissant
    sorted_tasks = sorted(tasks.keys(), key=lambda t: -ranks[t])

    ready_time = [0] * nb_machines  # disponibilité de chaque machine
    start_times = {}  # heure de début de chaque tâche
    end_times = {}    # heure de fin de chaque tâche
    schedule = {}     # affectation des tâches aux machines

    for task in sorted_tasks:
        # Calcule la date à laquelle la tâche peut commencer (tous les prédécesseurs doivent être terminés)
        preds = precedences.get(task, [])
        ready = max((end_times.get(p, 0) for p in preds), default=0)

        # Choisit la machine qui peut exécuter la tâche le plus tôt
        best_machine = min(
            range(nb_machines),
            key=lambda m: max(ready, ready_time[m])
        )

        start = max(ready_time[best_machine], ready)
        end = start + tasks[task]
        start_times[task] = start
        end_times[task] = end

        # Ajoute la tâche au planning de la machine choisie
        if best_machine not in schedule:
            schedule[best_machine] = []
        schedule[best_machine].append((task, start, end))

        # Met à jour la disponibilité de la machine
        ready_time[best_machine] = end

    # Le makespan (Cmax) est le temps de fin de la dernière tâche terminée
    cmax = max(end_times.values())
    return schedule, cmax, start_times, end_times

def plot_dag(precedences, start_times, end_times):
    G = nx.DiGraph()

    # Ajouter les nœuds avec labels enrichis
    for task in precedences:
        start = int(start_times.get(task, 0))
        end = int(end_times.get(task, 0))
        G.add_node(task, label=f"T{task}\n{start}/{end}")

    # Ajouter les arcs avec durées
    for task, deps in precedences.items():
        for dep in deps:
            G.add_edge(dep, task)

    pos = nx.spring_layout(G, seed=42)

    # Dessiner le graphe avec les labels
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=1000, arrows=True)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=11)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=9)

    plt.title("Graphe des dépendances")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Ordonnancement avec HEFT")
    parser.add_argument('-n', type=int, default=10, help='Nombre de tâches')
    parser.add_argument('-p', type=float, default=0.35, help="Probabilité de dépendance entre tâches")
    parser.add_argument('-m', type=int, default=4, help="Nombre de machines")
    parser.add_argument('-o', type=str, default='resultats.txt', help="Nom du fichier de sortie")
    args = parser.parse_args()

    N = args.n
    P = args.p
    NB_MACHINES = args.m
    OUTPUT_FILE = args.o

    tasks, precedences = generate_tasks_and_precedences(N, P)
    schedule, cmax, start_times, end_times = heft_scheduler(tasks, precedences, NB_MACHINES)

    # Affiche le planning final
    # for m in schedule:
    #     print(f"Machine {m}:")
    #     for t, s, e in schedule[m]:
    #         print(f"  Task {t}: {s} -> {e}")
    # print("Cmax =", cmax)

    # plot_dag(precedences, start_times, end_times)

    # Écriture des résultats dans un fichier
    with open(OUTPUT_FILE, 'w') as f:
        f.write(f"0, {N}, {P}, {NB_MACHINES}, {cmax}\n")

    # Affiche les résultats à l'écran
    # print(f"Nombre de tâches (n): {N}")
    # print(f"Probabilité de dépendance (p): {P}")
    # print(f"Nombre de machines (m): {NB_MACHINES}")
    # print(f"Cmax: {cmax}")
    print(0, N,P,NB_MACHINES,cmax)

if __name__ == "__main__":
    main()

# python3 ErdosRenyi.py -n 10 -p 0.35 -m 4 -o resultats.txt
