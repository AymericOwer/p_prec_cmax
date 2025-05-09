import random

def generate_gnp_dag(n, p):
    """Génère un DAG aléatoire à n sommets avec une probabilité p pour chaque arête (i -> j) avec i < j."""
    matrice = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n): 
            if random.random() < p:
                matrice[i][j] = 1

    return matrice

n = 25
p = 0.65
dag = generate_gnp_dag(n, p)

for row in dag:
    print(row)