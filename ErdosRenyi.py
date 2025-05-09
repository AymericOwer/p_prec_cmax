import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch


def generate_gnp_dag(n, p):
    """Génère un DAG aléatoire à n sommets avec une probabilité p pour chaque arête (i -> j) avec i < j."""
    matrice = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                matrice[i][j] = 1
    return matrice


def generate_tasks_and_precedences(n, p):
    matrix = generate_gnp_dag(n, p)

    successors = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                successors[i].append(j)

    # Inverser pour obtenir les dépendances (enfants → parents)
    precedences = {i: [] for i in range(n)}
    for parent, children in successors.items():
        for child in children:
            precedences[child].append(parent)

    # Générer un WCET aléatoire pour chaque tâche (par exemple entre 1 et 10)
    tasks = {i: random.randint(1, 10) for i in range(n)}

    return tasks, precedences


def build_successors(precedences):
    successors = {}
    for task, preds in precedences.items():
        for p in preds:
            if p not in successors:
                successors[p] = []
            successors[p].append(task)
    return successors


def compute_ranks(tasks, precedences):
    successors = build_successors(precedences)
    ranks = {}

    def dfs(task):
        if task in ranks:
            return ranks[task]
        succs = successors.get(task, [])
        rank = tasks[task] + max((dfs(s) for s in succs), default=0)
        ranks[task] = rank
        return rank

    for task in tasks:
        dfs(task)

    return ranks


def heft_scheduler(tasks, precedences, nb_machines):
    ranks = compute_ranks(tasks, precedences)
    sorted_tasks = sorted(tasks.keys(), key=lambda t: -ranks[t])
    ready_time = [0] * nb_machines
    start_times = {}
    end_times = {}
    schedule = {}

    for task in sorted_tasks:
        preds = precedences.get(task, [])
        ready = max((end_times.get(p, 0) for p in preds), default=0)

        best_machine = min(
            range(nb_machines),
            key=lambda m: max(ready, ready_time[m])
        )

        start = max(ready_time[best_machine], ready)
        end = start + tasks[task]
        start_times[task] = start
        end_times[task] = end

        if best_machine not in schedule:
            schedule[best_machine] = []
        schedule[best_machine].append((task, start, end))

        ready_time[best_machine] = end

    cmax = max(end_times.values())
    return schedule, cmax, start_times, end_times


def plot_dag(precedences, start_times, end_times):
    G = nx.DiGraph()

    for task, deps in precedences.items():
        start = int(start_times.get(task, 0))
        end = int(end_times.get(task, 0))
        G.add_node(task, label=f"T{task}\n{start}/{end}")

    for task, deps in precedences.items():
        for dep in deps:
            duration = int(start_times.get(task, 0) - end_times.get(dep, 0))
            G.add_edge(dep, task, label=str(duration))

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1000, node_shape='o', ax=ax)

    for node, (x, y) in pos.items():
        label = G.nodes[node]['label']
        plt.text(x, y, label, ha='center', va='center', fontsize=11)

    for u, v in G.edges():
        x_start, y_start = pos[u]
        x_end, y_end = pos[v]

        dx = x_end - x_start
        dy = y_end - y_start
        length = (dx**2 + dy**2)**0.5
        shrink_ratio = 0.1

        shrink_x = dx * shrink_ratio
        shrink_y = dy * shrink_ratio

        arrow = FancyArrowPatch(
            (x_start + shrink_x, y_start + shrink_y),
            (x_end - shrink_x, y_end - shrink_y),
            arrowstyle='-|>',
            mutation_scale=20,
            color='black',
            linewidth=1.5,
            connectionstyle='arc3,rad=0.05'
        )
        ax.add_patch(arrow)

        label = G.edges[u, v]['label']
        mid_x = (x_start + x_end) / 2
        mid_y = (y_start + y_end) / 2
        plt.text(mid_x, mid_y, label, fontsize=9, color='red', ha='center')

    plt.title("Graphe des dépendances")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    N = 10
    P = 0.35
    NB_MACHINES = 4

    tasks, precedences = generate_tasks_and_precedences(N, P)
    schedule, cmax, start_times, end_times = heft_scheduler(tasks, precedences, NB_MACHINES)

    for m in schedule:
        print(f"Machine {m}:")
        for t, s, e in schedule[m]:
            print(f"  Task {t}: {s} -> {e}")
    print("Cmax =", cmax)

    plot_dag(precedences, start_times, end_times)
