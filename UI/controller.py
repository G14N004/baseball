import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        anno = None
        try:
            anno = int(self._view._ddAnno.value)
            self._model.buildGrafo(anno)
            self._view._txt_result.controls.append(ft.Text(f"Grafo creato correttamnete , ha {self._model.getNumNodi()} nodi e {self._model.getNumArchi()}"))
            self._view.update_page()

        except ValueError:
            self._view._txt_result.controls.append(ft.Text("valore invalido"))
            self._view.update_page()




    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        try:
            squadra = int(self._view._ddSquadra.value)
            tuplaSquadra=self._model.getIdMap()[squadra]
            self._view._txt_result.controls.append(ft.Text(f"per la Squadra {tuplaSquadra[1]} i suoi  vicini con peso decrescente sono : "))
            neigh=self._model.trovaViciniConNeigh(tuplaSquadra)
            neigh.sort(key=lambda x: x[1],reverse=True)
            #first5=neigh[:5]
            for elm in neigh:
                self._view._txt_result.controls.append(ft.Text(f"{elm[0]} --> {elm[1]}"))
            self._view.update_page()


        except ValueError:
            self._view._txt_result.controls.append(ft.Text("scegli una squadra"))




    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        if self._view._ddSquadra.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona prima una squadra dalla tendina!"))
            self._view.update_page()
            return
        id_squadra_scelta = int(self._view._ddSquadra.value)
        id_map = self._model.getIdMap()

        # Controllo di sincronizzazione del grafo
        if id_squadra_scelta not in id_map:
            self._view._txt_result.controls.append(
                ft.Text("Il grafo non è aggiornato per l'anno selezionato. Clicca prima su 'Crea Grafo'!")
            )
            self._view.update_page()
            return
        squadra_partenza = self._model.getIdMap()[id_squadra_scelta]
        if squadra_partenza is None:
            self._view._txt_result.controls.append(ft.Text("Squadra non trovata nel grafo."))
            self._view.update_page()
            return

        percorso , peso = self._model.getPercorsoMassimo(squadra_partenza)
        if len(percorso) <= 1:
            self._view._txt_result.controls.append(
                ft.Text(f"Nessun percorso decrescente trovato a partire da {squadra_partenza[1]}.")
            )
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text(f" il pecorso di peso massimo per {squadra_partenza} è : {percorso} --> con peso {peso}"))
        self._view.update_page()



    def fillDDAnno(self):
        anni=self._model.getAnni()
        for a in anni :
            self._view._ddAnno.options.append(ft.dropdown.Option(key=a, text=a))
        self._view.update_page()

    def handleAnnoSelezionato(self,e):
        self._view._txtOutSquadre.controls.clear()
        self._view._ddSquadra.options.clear()
        if self._view._ddAnno.value is None:
            # Esci silenziosamente perché l'app è appena partita
            # e l'utente non ha ancora scelto l'anno
            return

            # 2. Se arriviamo qui, c'è qualcosa nella dropdown, procediamo con sicurezza

        anno=None
        try:
            anno=int(self._view._ddAnno.value)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text("seleziona un anno "))
            self._view.update_page()
            return

        squadre=self._model.getSquadre(anno)

        for s in squadre :
            self._view._ddSquadra.options.append(ft.dropdown.Option(key=s[0], text=s[1]))
            self._view._txtOutSquadre.controls.append(ft.Text(f"{s}"))
        self._view.update_page()
