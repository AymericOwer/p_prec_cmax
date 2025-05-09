import random
import task_pb2

def generate_random_dag(n, p, wcet_range=(1, 10)):
    task_graph = task_pb2.TaskGraph()

    for i in range(n):
        task = task_graph.tasks.add()
        task.id = i
        task.wcet = random.randint(*wcet_range)

        # Ajoute des dépendances vers des tâches plus anciennes (i.e. j < i)
        for j in range(i):
            if random.random() < p:
                task.dependencies.append(j)

    return task_graph

def save_task_graph(task_graph, filename="exemple.bin"):
    with open("exemple.bin", "wb") as f:
        f.write(task_graph.SerializeToString())

if __name__ == "__main__":
    n = 10        # nombre de tâches
    p = 0.3       # probabilité d'un arc
    wcet_range = (1, 10)

    graph = generate_random_dag(n, p, wcet_range)
    save_task_graph(graph)
    print(f"{n} tâches générées avec p = {p} et sauvegardées dans exemple.bin")
