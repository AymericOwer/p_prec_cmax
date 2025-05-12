import csv

moyenne = []
bloc = []
moy_courant = []

with open("resultats.csv", 'r') as file:
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

x=0
for ligne in bloc:
    ligne.append(ret[x])
    x+=1

with open("opt.csv", 'a') as file:
    w = csv.writer(file)
    for ligne in bloc:
        w.writerow(ligne)
    
