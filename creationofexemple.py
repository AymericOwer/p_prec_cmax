import task_pb2

# Crée une instance de TaskGraph
task_graph = task_pb2.TaskGraph()

# Ajoute quelques tâches manuellement
t1 = task_graph.tasks.add()
t1.id = 1
t1.wcet = 3
t1.dependencies.extend([])

t2 = task_graph.tasks.add()
t2.id = 2
t2.wcet = 2
t2.dependencies.extend([1])

t3 = task_graph.tasks.add()
t3.id = 3
t3.wcet = 4
t3.dependencies.extend([1])

t4 = task_graph.tasks.add()
t4.id = 4
t4.wcet = 2
t4.dependencies.extend([2, 3])

# Sauvegarde dans le fichier exemple.bin
with open("exemple.bin", "wb") as f:
    f.write(task_graph.SerializeToString())
