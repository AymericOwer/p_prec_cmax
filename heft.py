from collections import defaultdict
import task_pb2  # Généré via protoc
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    NB_MACHINES = 4
    tasks, precedences = load_task_graph("exemple.bin")
    schedule, cmax = heft_scheduler(tasks, precedences, NB_MACHINES)

    for m in schedule:
        print(f"Machine {m}:")
        for t, s, e in schedule[m]:
            print(f"  Task {t}: {s} -> {e}")
    print("Cmax =", cmax)

    plot_schedule(schedule)
