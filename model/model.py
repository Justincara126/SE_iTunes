import copy
from copy import deepcopy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.dao = DAO()
        self.g=nx.Graph()
    def get_album(self,minuti):

        self.dizionario_album=self.dao.get_album(minuti)
        lista_id=[]
        for chiave in self.dizionario_album:
            self.g.add_node(self.dizionario_album[chiave])
            lista_id.append(chiave)
        connessioni=self.dao.get_edges(lista_id)
        for coppia in connessioni:
            self.g.add_edge(self.dizionario_album[coppia[0]],self.dizionario_album[coppia[1]])
        print(self.g)

        return self.dizionario_album

    def get_componente_connessa(self,id_album):
        album=self.dizionario_album[id_album]
        lista_album_connessi=nx.dfs_tree(self.g,album)
        # è un digrap
        print(lista_album_connessi.nodes())
        minuti_totali=sum(album.durata for album in lista_album_connessi.nodes())
        return len(lista_album_connessi),round(minuti_totali/(60*1000),2)


    def get_perscorso_maggiore(self,id_album,peso_massimo):
        album=self.dizionario_album[id_album]
        grafo_filtrato=nx.dfs_tree(self.g,album)
        self.peso_maggiore=-1
        self.perscorso_migliore=[]
        peso=album.durata/(60*1000)
        self.ricorsione([album],grafo_filtrato,peso,peso_massimo)
        print(self.perscorso_migliore)
        return self.perscorso_migliore,self.peso_maggiore

    def ricorsione(self,parziale,grafo_filtrato,peso,peso_massimo):
        if peso>peso_massimo:
            return
        if peso>self.peso_maggiore:
            self.peso_maggiore=peso
            self.perscorso_migliore=parziale.copy()
        for vicino in grafo_filtrato.neighbors(parziale[-1]):
            if vicino not in parziale:
                print(vicino)
                parziale.append(vicino)
                peso=peso+(vicino.durata/(60*1000))
                self.ricorsione(parziale,grafo_filtrato,peso,peso_massimo)
                parziale.pop()




