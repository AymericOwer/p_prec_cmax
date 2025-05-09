from collections import defaultdict
import task_pb2  # Généré via protoc
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch

def load_task_graph(bin_path):
    task_graph = task_pb2.TaskGraph()
    with open(bin_path, "rb") as f:
        task_graph.ParseFromString(f.read())
    
    tasks = {task.id: task.wcet for task in task_graph.tasks}
    precedences = {task.id: list(task.dependencies) for task in task_graph.tasks}
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
    return schedule, cmax


def plot_schedule(schedule):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots()
    colors = plt.cm.get_cmap('tab20', sum(len(v) for v in schedule.values()))

    task_id = 0
    for m, tasks in schedule.items():
        for t, start, end in tasks:
            ax.broken_barh([(start, end - start)], (m * 10, 9),
                           facecolors=colors(task_id))
            ax.text(start + (end - start) / 2, m * 10 + 4.5, f"T{t}",
                    va='center', ha='center', fontsize=8, color='white')
            task_id += 1

    ax.set_yticks([m * 10 + 4.5 for m in schedule.keys()])
    ax.set_yticklabels([f"Machine {m}" for m in schedule.keys()])
    ax.set_xlabel("Temps")
    ax.set_title("Planning HEFT")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def plot_dag(precedences, start_times, end_times):
    G = nx.DiGraph()

    # Créer les nœuds avec labels enrichis
    for task, deps in precedences.items():
        start = int(start_times.get(task, 0))
        end = int(end_times.get(task, 0))
        G.add_node(task, label=f"T{task}\n{start}/{end}")

    # Ajouter les arcs avec durée
    for task, deps in precedences.items():
        for dep in deps:
            duration = int(start_times.get(task, 0) - end_times.get(dep, 0))
            G.add_edge(dep, task, label=str(duration))

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Dessiner les nœuds en cercles plus petits
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=1000, node_shape='o', ax=ax)

    # Affichage des étiquettes dans les nœuds
    for node, (x, y) in pos.items():
        label = G.nodes[node]['label']
        plt.text(x, y, label, ha='center', va='center', fontsize=11)

    # Dessiner les flèches manuellement pour éviter qu'elles soient cachées
    for u, v in G.edges():
        x_start, y_start = pos[u]
        x_end, y_end = pos[v]

        # Décalage pour ne pas toucher les bords du cercle
        dx = x_end - x_start
        dy = y_end - y_start
        length = (dx**2 + dy**2)**0.5
        shrink_ratio = 0.1  # ajustable

        # Appliquer le décalage
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

        # Étiquette de durée au milieu de l’arc
        label = G.edges[u, v]['label']
        mid_x = (x_start + x_end) / 2
        mid_y = (y_start + y_end) / 2
        plt.text(mid_x, mid_y, label, fontsize=9, color='red', ha='center')

    plt.title("Graphe des dépendances")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    NB_MACHINES = 4
    tasks, precedences = load_task_graph("exemple.bin")
    schedule, cmax = heft_scheduler(tasks, precedences, NB_MACHINES)

    start_times = {}
    end_times = {}
    for m in schedule:
        for t, s, e in schedule[m]:
            start_times[t] = s
            end_times[t] = e

    for m in schedule:
        print(f"Machine {m}:")
        for t, s, e in schedule[m]:
            print(f"  Task {t}: {s} -> {e}")
    print("Cmax =", cmax)

    plot_dag(precedences, start_times, end_times)
    # plot_schedule(schedule)
