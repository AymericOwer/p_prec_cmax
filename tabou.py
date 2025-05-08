import random
from collections import deque


def makespan(solution, durations):
    return max(
        sum(durations[t] for t in machine)
        for machine in solution
    )


def generer_voisins(solution):
    voisins = []
    for i, machine in enumerate(solution):
        for j, tache in enumerate(machine):
            for k in range(len(solution)):
                if k != i: 
                    nouvelle_solution = [list(m) for m in solution]
                    nouvelle_solution[i].pop(j)
                    nouvelle_solution[k].append(tache)
                    voisins.append(nouvelle_solution)
    return voisins



def tabou_search(durations, solution_init, max_iterations=100, taille_tabou=7):
    solution_actuelle = [list(m) for m in solution_init]
    meilleure_solution = [list(m) for m in solution_init]
    meilleur_makespan = makespan(meilleure_solution, durations)

    liste_tabou = deque(maxlen=taille_tabou)

    for iteration in range(max_iterations):
        voisins = generer_voisins(solution_actuelle)
        voisin_choisi = None
        meilleur_voisin_score = float('inf')
        mouvement_choisi = None

        for voisin in voisins:
            mouvement = detect_mouvement(solution_actuelle, voisin)
            score = makespan(voisin, durations)

            if mouvement not in liste_tabou or score < meilleur_makespan:
                if score < meilleur_voisin_score:
                    meilleur_voisin_score = score
                    voisin_choisi = voisin
                    mouvement_choisi = mouvement

        if voisin_choisi is None:
            break  # Pas de voisin acceptable trouvé

        solution_actuelle = [list(m) for m in voisin_choisi]

        if meilleur_voisin_score < meilleur_makespan:
            meilleure_solution = [list(m) for m in voisin_choisi]
            meilleur_makespan = meilleur_voisin_score

        liste_tabou.append(mouvement_choisi)

        print(f"Itération {iteration+1} : Makespan = {meilleur_makespan}")

    return meilleure_solution, meilleur_makespan

def detect_mouvement(sol1, sol2):
    for i in range(len(sol1)):
        for t in sol1[i]:
            if t not in sol2[i]:
                for j in range(len(sol2)):
                    if t in sol2[j]:
                        return (t, i, j)  # tache déplacée de machine i à j
    return None


durations = [2, 3, 6, 4, 5, 1, 8]

solution_init = [
    [0,1,4,3],
    [2,6,5],
    [6]
]

best_sol, best_makespan = tabou_search(durations, solution_init)
print("Meilleure solution :", best_sol)
print("Makespan :", best_makespan)
