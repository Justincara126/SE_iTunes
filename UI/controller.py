import flet as ft

from UI.alert import AlertManager
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        try:
            minuti=int(self._view.txt_durata.value)
            print(minuti)
            dizionario_album=self._model.get_album(minuti)
            self._view.dd_album.options.clear()
            self._view.pulsante_analisi_comp.disabled = False

            for chiave in dizionario_album:
                self._view.dd_album.options.append(ft.dropdown.Option(key=chiave,text=dizionario_album[chiave]))
            self._view.page.update()
            self._view.lista_visualizzazione_1.controls.clear()
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f'{self._model.g}'))


        except ValueError:
            self._view.show_alert('---inserire un numero---')




    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO
        try:
            id_album=int(self._view.dd_album.value)
            print(id_album)
        except ValueError:
            self._view.show_alert('error')


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        try:
            id_album=int(self._view.dd_album.value)
            num,durata=self._model.get_componente_connessa(id_album)
            self._view.lista_visualizzazione_2.controls.clear()
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Ci sono {num} altri album collegati con durata totale di {durata}'))
            self._view.page.update()

        except ValueError:
            self._view.show_alert('---inserire un album---')




    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        try:
            id_album = int(self._view.dd_album.value)
            minuti=int(self._view.txt_durata_totale.value)
            print(id_album,minuti)
            percorso,peso=self._model.get_perscorso_maggiore(id_album,minuti)
            self._view.lista_visualizzazione_3.controls.clear()
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f' Durata totale: {peso} minuti, con {len(percorso)} album'))
            for i in percorso:
                self._view.lista_visualizzazione_3.controls.append(ft.Text(f' {i} '))
            self._view.page.update()


        except ValueError:
            self._view.show_alert('error')

