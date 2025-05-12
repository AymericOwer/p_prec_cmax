import subprocess
import csv

n_values = list(range(1,51, 5))  # Exemple de tailles de tâches
p_values = [0.25, 0.5, 0.75]   # Probabilités de dépendance
m_values = [4]  # Nombre de machines
INSTANCE = list(range(21))

def run_erdos_renyi_script(n, p, m, output_file):
    command = [
        "python3", "ErdosRenyi.py", 
        "-n", str(n), 
        "-p", str(p), 
        "-m", str(m),
        "-o", output_file
    ]
    subprocess.run(command)

def run_topo_script(n, p, m, output_file):
    command = [
        "python3", "topo.py", 
        "-n", str(n), 
        "-p", str(p), 
        "-m", str(m),
        "-o", output_file
    ]
    subprocess.run(command)


def generate_results():
    resultsHEFT = []
    resultsTOPO = []
    for n in n_values:
        for p in p_values:
            for m in m_values:
                for i in INSTANCE:
                    output_file = "resultats.csv"
                    run_erdos_renyi_script(n, p, m, output_file)
                    # Lire le fichier CSV généré et ajouter les résultats à la liste
                    with open(output_file, 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if row:
                                resultsHEFT.append(row)
                    run_topo_script(n, p, m, output_file)
                    with open(output_file, 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if row:
                                resultsTOPO.append(row)
                resultsHEFT.append("--")
                resultsTOPO.append("--")
    return resultsHEFT, resultsTOPO


def main():
    resultsHEFT, resultsTOPO = generate_results()
    # Sauvegarder les résultats dans un fichier CSV
    with open('resultats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(resultsHEFT)
        writer.writerows(resultsTOPO)


if __name__ == "__main__":
    main()