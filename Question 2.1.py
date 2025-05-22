import pandas as pd
from itertools import product
from collections import defaultdict, deque

pd.options.display.max_rows = 9999

df = pd.read_csv('data.csv', sep=';')

Stations = df.drop(columns=['Identifiant station','Lien vers les mesures en direct', 'Mesures d’amélioration mises en place ou prévues','air','actions','Incertitude','Recommandation de surveillance','Action(s) QAI en cours','Action(s) QAI en cours','Durée des mesures','stop_lon','stop_lat','point_geo','niveau_pollution','niveau','pollution_air','Niveau de pollution aux particules','Niveau de pollution'])
Stations.drop_duplicates(inplace=True)
Stations.dropna(how='all',inplace=True)

#J'ai gardé les RER


# Liste des stations
stations_list = Stations.iloc[:, 0].unique()

# Produit cartésien de toutes les paires (plus efficace) en vérifient que d et différent de a et sans pair (d<a)
Graph = pd.DataFrame([
    {"Départ": d, "Arrivée": a, "Bool": False}
    for d, a in product(stations_list, repeat=2) if d < a
])

# Nettoyer les espaces avant les nom des lignes
Stations["Nom de la Station"] = Stations["Nom de la Station"].str.strip()
Stations["Nom de la ligne"] = Stations["Nom de la ligne"].str.strip()
Graph["Départ"] = Graph["Départ"].str.strip()
Graph["Arrivée"] = Graph["Arrivée"].str.strip()


# graphe est un dictionnaire de voisin(sur la même ligne ou les même ligne si intersection type Bastille)
graphe = defaultdict(set)

for ligne, groupe in Stations.groupby("Nom de la ligne"):
    stations = groupe["Nom de la Station"].tolist()
    for i in range(len(stations)):
        for j in range(i + 1, len(stations)):
            graphe[stations[i]].add(stations[j])
            graphe[stations[j]].add(stations[i])


#Identifier les composantes connexes via BFS
station_to_component = {}
component_id = 0

for station in graphe:
    if station not in station_to_component:
        queue = deque([station])
        while queue:
            current = queue.popleft()
            if current not in station_to_component:
                station_to_component[current] = component_id
                for voisin in graphe[current]:
                    if voisin not in station_to_component:
                        queue.append(voisin)
        component_id += 1

#Test de connectivité
def est_connecte(dep, arr):
    return station_to_component.get(dep) == station_to_component.get(arr)

#Appliquer à tous les trajets True si réalisable
Graph["Bool"] = Graph.apply(lambda row: est_connecte(row["Départ"], row["Arrivée"]), axis=1)


Stations.to_csv("stations_metro.csv", index=False, encoding='utf-8-sig',sep=';')
Graph.to_csv("graph_stations.csv", index=False, sep=';', encoding='utf-8-sig')

#Pas efficace donc abondonnées
#Graph=pd.DataFrame(columns=["Départ", "Arrivée", "Bool"])
#for i in range (len(Stations)):
#    for j in range (len(Stations)):
#        if Stations.iloc[i,0] != Stations.iloc[j,0]:
#            Graph.loc[len(Graph)]=[Stations.iloc[i,0],Stations.iloc[j,0],False]

# Fonction de recherche : est-ce qu'on peut atteindre "arrivée" depuis "depart"
#def trajet_possible(depart, arrivee):
 #   if depart not in graphe or arrivee not in graphe:
  #      return False
   # vus = set()
    #file = deque([depart])
    #while file:
    #    courant = file.popleft()
    #    if courant == arrivee:
    #        return True
    #    vus.add(courant)
    #    for voisin in graphe[courant]:
    #        if voisin not in vus:
    #            file.append(voisin)
    #return False

# Appliquer à chaque ligne  (on refait la recherche à chaque fois)
#Graph["Bool"] = Graph.apply(lambda row: trajet_possible(row["Départ"], row["Arrivée"]), axis=1)
