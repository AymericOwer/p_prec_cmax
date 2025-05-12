import matplotlib.pyplot as plt
import csv

def plot_results(results):
    # Extraire les données
    color_values = [float(row[0]) for row in results]  # valeur pour la couleur (entre 0 et 1)
    n_values = [int(row[1]) for row in results]        # nombre de tâches
    cmax_values = [float(row[4]) for row in results]     # Cmax

    # Tracer le graphique
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        n_values,
        cmax_values,
        c=color_values,
        cmap='bwr',  # bleu-blanc-rouge pour une échelle entre 0 (bleu) et 1 (rouge)
        s=150,
        alpha=0.7
    )
    plt.title('Cmax en fonction de n')
    plt.xlabel('n (Nombre de tâches)')
    plt.ylabel('Cmax')
    plt.colorbar(scatter, label='0 : HEFT ; 1 : Topologie')
    plt.grid(True)
    plt.show()

results = []
with open("Data/preprocess/opt.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row:
            results.append(row)

plot_results(results)