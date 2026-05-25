from copy import deepcopy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap={}
        #for elm in self.getSquadre(anno):
        #    self._idMap[elm[0]]=elm
        self._bestPath=[]
        self._bestPeso=0

    def getPercorsoMassimo(self, nodo_partenza):
        """Metodo pubblico per attivare la ricorsione"""
        self._bestPath = []
        self._bestWeight = 0

        # Il cammino parziale inizia con il solo nodo di partenza
        parziale = [nodo_partenza]

        # Avviamo la ricorsione.
        # All'inizio non abbiamo un arco precedente, quindi passiamo un peso infinito (float('inf'))
        self._ricorsione(parziale, 4876237686786463243432344, 0)

        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale, peso_precedente, peso_accumulato):
        # CORRETTO: Usiamo 'peso_accumulato' per verificare se abbiamo battuto il record attuale
        if peso_accumulato > self._bestWeight:
            self._bestWeight = peso_accumulato
            self._bestPath = deepcopy(parziale)

            # Esploriamo i vicini dell'ultimo nodo inserito in parziale
        nodo_corrente = parziale[-1]

        for vicino, attributi in self._grafo[nodo_corrente].items():
            peso_arco = attributi.get('weight', 0)

            # Vincoli: no duplicati e peso strettamente decrescente
            if vicino not in parziale and peso_arco < peso_precedente:
                parziale.append(vicino)

                # PASSO RICORSIVO: passiamo la nuova somma (peso_accumulato + peso_arco)
                self._ricorsione(parziale, peso_arco, peso_accumulato + peso_arco)

                # BACKTRACKING
                parziale.pop()



    def getAnni(self):
        return DAO.getAllAnni()

    def getSquadre(self,anno):
        return DAO.getSquadre(anno)

    def getSalari(self,anno):
        return DAO.getSalario(anno)

    def buildGrafo(self,anno):
        self._grafo.clear()
        self._idMap.clear()
        nodi = self.getSquadre(anno)
        for n in nodi :
            self._grafo.add_node(n)
            self._idMap[n[0]]=n



        mapSalari = self.getSalari(anno)
        for i in range(len(nodi)):
            for j in range(i+1,len(nodi)):
                s1=nodi[i]
                s2=nodi[j]
                salari_s1=mapSalari.get(s1[0],0)
                salari_s2=mapSalari.get(s2[0],0)
                peso_arco=salari_s1+salari_s2
                self._grafo.add_edge(s1,s2,weight=peso_arco)


    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    def trovaViciniConNeigh(self,sorgente):
        ris=[]
        if self._grafo.has_node(sorgente):
            for vicino in self._grafo.neighbors(sorgente):
                peso = self._grafo[sorgente][vicino].get('weight',0)
                ris.append((vicino,peso))
        return ris

    def trovaViciniAlternativo(self,sorgente):
        ris = []
        if self._grafo.has_node(sorgente):
            for vicino,attributi in self._grafo[sorgente].items():
                peso = attributi.get('weight',0)
                ris.append((vicino,peso))
        return ris
    def getIdMap(self):
        return self._idMap
