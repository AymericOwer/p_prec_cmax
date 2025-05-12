import subprocess
import csv
import matplotlib.pyplot as plt
import numpy as np


# Fonction pour exécuter le script ErdosRenyi.py avec différents paramètres
def run_erdos_renyi_script(n, p, m, output_file):
    command = [
        "python3", "ErdosRenyi.py", 
        "-n", str(n), 
        "-p", str(p), 
        "-m", str(m),
        "-o", output_file
    ]
    subprocess.run(command)

# Générer les résultats avec plusieurs valeurs de n, p et m
def generate_results():
    results = []
    n_values = list(range(1,101, 5))  # Exemple de tailles de tâches
    p_values = np.arange(0.1, 0.55, 0.02)   # Probabilités de dépendance
    m_values = [4]  # Nombre de machines
    for n in n_values:
        for p in p_values:
            for m in m_values:
                output_file = "resultats.csv"
                run_erdos_renyi_script(n, p, m, output_file)
                # Lire le fichier CSV généré et ajouter les résultats à la liste
                with open(output_file, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row:
                            results.append(row)
    return results

# Générer un graphe à partir des résultats CSV
def plot_results(results):
    # Extraire les données pour les axes du graphe
    n_values = [int(row[0]) for row in results]
    p_values = [float(row[1]) for row in results]
    m_values = [int(row[2]) for row in results]
    cmax_values = [int(row[3]) for row in results]

    # Exemple de graphique: Cmax en fonction de n
    plt.figure(figsize=(10, 6))
    plt.scatter(n_values, cmax_values, c=p_values, cmap='plasma', label="Cmax",s=100, alpha=0.7)
    plt.title('Cmax en fonction de n')
    plt.xlabel('n (Nombre de tâches)')
    plt.ylabel('Cmax')
    plt.colorbar(label='p (Probabilité de dépendance)')
    plt.show()

def main():
    results = generate_results()
    # Sauvegarder les résultats dans un fichier CSV
    with open('resultats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(results)

    # Générer le graphe à partir des résultats
    plot_results(results)

if __name__ == "__main__":
    main()
