"""
Statistiques multivariées déstinées à comparer nos différents modèles.
Les données traitées se trouvent par défaut à l'emplacement ~/Documents/resultats.pkl.
Ces données ont été préalablement générées avec le script bench.py.
"""

import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import scatter_matrix

res = pd.read_pickle("~/Documents/resultats.pkl")

res.boxplot(column=['lpm'], by='Modèle')
res.boxplot(column=['Nb collisions'], by='Modèle')
res.boxplot(column=['Distance moyenne'], by='Modèle')
res.boxplot(column=['Distance max'], by='Modèle')

for key in ["lpm", "Nb collisions", "Distance moyenne", "Distance max"]:
	var1 = list(res[res["Modèle"] == "1"][key])
	var1_1 = list(res[res["Modèle"] == "1.1"][key])
	var2 = list(res[res["Modèle"] == "2"][key])
	var3 = list(res[res["Modèle"] == "3"][key])
	var1.sort()
	var1_1.sort()
	var2.sort()
	var3.sort()

	result = pd.DataFrame({key+"1": var1, key+"1.1": var1_1, key+"2": var2, key+"3": var3})

	scatter_matrix(result, figsize=(6, 6), diagonal='kde')

	print(result.corr())

plt.show()
