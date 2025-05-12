import random
import argparse

def generate_gnp_dag(n, p):
    matrice = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                matrice[i][j] = 1
    return matrice

def generate_tasks_and_precedences(n, p):
    matrix = generate_gnp_dag(n, p)
    precedences = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                precedences[j].append(i)
    tasks = {i: random.randint(1, 10) for i in range(n)}
    return tasks, precedences

def calcul_cmax_avec_machines(PRED, COUT, num_machines):
    SUCC = {t: [] for t in PRED}
    in_degree = {t: len(PRED[t]) for t in PRED}
    for t in PRED:
        for p in PRED[t]:
            SUCC[p].append(t)

    queue = [t for t in PRED if in_degree[t] == 0]
    ordre_topo = []

    while queue:
        u = queue.pop(0)
        ordre_topo.append(u)
        for v in SUCC.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    debut = {}
    fin = {}
    machines = [0] * num_machines
    affectation_machines = {}

    for t in ordre_topo:
        debut_t = 0 if not PRED[t] else max(fin[p] for p in PRED[t])
        machine_dispo = min(range(num_machines), key=lambda m: machines[m])
        debut_t = max(debut_t, machines[machine_dispo])
        fin_t = debut_t + COUT[t]
        machines[machine_dispo] = fin_t
        debut[t] = debut_t
        fin[t] = fin_t
        affectation_machines[t] = machine_dispo

    cmax = max(fin.values())
    return cmax, debut, fin, affectation_machines

# def afficher_par_machine(debut, fin, affectation_machines, cmax):
#     machine_tasks = {}
#     for task, machine in affectation_machines.items():
#         machine_tasks.setdefault(machine, []).append((task, debut[task], fin[task]))

#     for machine in sorted(machine_tasks):
#         print(f"Machine {machine}:")
#         for task, d, f in sorted(machine_tasks[machine], key=lambda x: x[1]):
#             print(f"  Task {task}: {d} -> {f}")
#     print(f"Cmax = {cmax}")


def ecrire_resultats_resume(file, n, p, num_machines, cmax):
    with open(file, "w") as f:
        f.write(f"1, {n}, {p}, {num_machines}, {cmax},\n")


# --- Partie exécutable ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ordonnancement de tâches avec contraintes de précédence sur plusieurs machines.")
    parser.add_argument("-n", type=int, required=True, help="Nombre de tâches")
    parser.add_argument("-p", type=float, required=True, help="Probabilité d'une arête dans le DAG")
    parser.add_argument("-m", type=int, required=True, help="Nombre de machines")
    parser.add_argument("-o", type=str, help="Fichier de sortie (optionnel)")

    args = parser.parse_args()

    tasks, precedences = generate_tasks_and_precedences(args.n, args.p)
    cmax, debut, fin, affectation_machines = calcul_cmax_avec_machines(precedences, tasks, args.m)
    # Affichage normal à l'écran
    # afficher_par_machine(debut, fin, affectation_machines, cmax)

    # Écriture dans le fichier si demandé
    if args.o:
        ecrire_resultats_resume(args.o, args.n, args.p, args.m, cmax)
        print(1, args.n,args.p,args.m,cmax)
    else:
        ecrire_resultats_resume("default.csv", args.n, args.p, args.m, cmax)
        print(1, args.n,args.p,args.m,cmax)
