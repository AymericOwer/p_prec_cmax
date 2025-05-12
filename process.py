import subprocess
import csv

n_values = list(range(1, 201, 5))  # Exemple de tailles de tâches
p_values = [0.25]   # Probabilités de dépendance
m_values = [3]     # Nombre de machines
INSTANCE = list(range(51))

def run_erdos_renyi_script(n, p, m, output_file):
    command = [
        "python3", "Algo/heft.py",
        "-n", str(n),
        "-p", str(p),
        "-m", str(m),
        "-o", output_file
    ]
    subprocess.run(command)

def run_topo_script(n, p, m, output_file):
    command = [
        "python3", "Algo/topo.py",
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
                    output_file = "Data/preprocess/resultats.csv"
                    run_erdos_renyi_script(n, p, m, output_file)
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
                resultsHEFT.append(['-', '-'])
                resultsTOPO.append(['-', '-'])
    return resultsHEFT + resultsTOPO  # on concatène les deux listes pour analyse ensuite

def post_process_results():
    moyenne = []
    bloc = []
    moy_courant = []

    with open("Data/preprocess/resultats.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row == ['-', '-']:
                if moy_courant:
                    moyenne.append(moy_courant)
                    moy_courant = []
            elif row:
                ligne = [row[0], row[1], row[2], row[3]]
                if ligne not in bloc:
                    bloc.append(ligne)
                moy = int(row[4])
                moy_courant.append(moy)

    ret = []
    for calc in moyenne:
        res = sum(calc) / len(calc)
        ret.append(res)

    x = 0
    for ligne in bloc:
        ligne.append(ret[x])
        x += 1

    with open("Data/preprocess/opt.csv", 'a', newline='') as file:
        w = csv.writer(file)
        for ligne in bloc:
            w.writerow(ligne)

def main():
    all_results = generate_results()

    # Sauvegarder dans le fichier intermédiaire
    with open("Data/preprocess/resultats.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_results)

    # Traitement postérieur
    post_process_results()

if __name__ == "__main__":
    main()
