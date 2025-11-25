from database.regione_DAO import RegioneDAO
from database.tour_DAO import TourDAO
from database.attrazione_DAO import AttrazioneDAO

class Model:
    def __init__(self):
        self.tour_map = {} # Mappa ID tour -> oggetti Tour
        self.attrazioni_map = {} # Mappa ID attrazione -> oggetti Attrazione

        self._pacchetto_ottimo = []
        self._valore_ottimo: int = -1
        self._costo = 0

        self._tour_attrazioni= {}
        # Caricamento
        self.load_tour()
        self.load_attrazioni()
        self.load_relazioni()

    @staticmethod
    def load_regioni():
        """ Restituisce tutte le regioni disponibili """
        return RegioneDAO.get_regioni()

    def load_tour(self):
        """ Carica tutti i tour in un dizionario [id, Tour]"""
        self.tour_map = TourDAO.get_tour()

    def load_attrazioni(self):
        """ Carica tutte le attrazioni in un dizionario [id, Attrazione]"""
        self.attrazioni_map = AttrazioneDAO.get_attrazioni()

    def load_relazioni(self):
        lista_dizionari_tour_attrazzione = TourDAO.get_tour_attrazioni()
        for dizionario in lista_dizionari_tour_attrazzione:
            for chiave,valore in dizionario.items():
                if chiave in self.tour_map.keys():
                    self._tour_attrazioni[chiave].append(valore)
        # creo un dizionario che ha come chiave il tour e come valori le attrazioni

        """
            Interroga il database per ottenere tutte le relazioni fra tour e attrazioni e salvarle nelle strutture dati
            Collega tour <-> attrazioni.
            --> Ogni Tour ha un set di Attrazione.
            --> Ogni Attrazione ha un set di Tour.
        """

    def genera_pacchetto(self, id_regione: str, max_giorni: int = None, max_budget: float = None):
        """
        Calcola il pacchetto turistico ottimale per una regione rispettando i vincoli di durata, budget e attrazioni uniche.
        :param id_regione: id della regione
        :param max_giorni: numero massimo di giorni (può essere None --> nessun limite)
        :param max_budget: costo massimo del pacchetto (può essere None --> nessun limite)

        :return: self._pacchetto_ottimo (una lista di oggetti Tour)
        :return: self._costo (il costo del pacchetto)
        :return: self._valore_ottimo (il valore culturale del pacchetto)
        """
        self._pacchetto_ottimo = []
        self._costo = 0
        self._valore_ottimo = -1

        for id_tour,attrazioni in self._tour_attrazioni.items():
            tour = self.tour_map[id_tour]
            if tour["id_regione"]==id_regione and tour["durata_giorni"]<= max_giorni and tour["costo"]<= max_budget:
                self._pacchetto_ottimo.append(tour)
                self._costo += tour["costo"]
                for attrazione in attrazioni:
                    valore = self.attrazioni_map[attrazione]["valore_culturale"]
                    valore_tot = sum(valore)
                    self._valore_ottimo += valore_tot

        return self._pacchetto_ottimo, self._costo, self._valore_ottimo

    def _ricorsione(self, start_index: int, pacchetto_parziale: list, durata_corrente: int, costo_corrente: float, valore_corrente: int, attrazioni_usate: set):
        if start_index==len(self._pacchetto_ottimo):
            self._pacchetto_ottimo = pacchetto_parziale
            self._costo = costo_corrente
            self._valore_ottimo = valore_corrente
        else:
            # inizio con l'indice zero e ogni ricorsione lo incremento di uno
            start_index = 0
            #for tour in self._pacchetto_ottimo:
            #    pacchetto_parziale.append(tour)
            #    durata_corrente += tour["durata_giorni"]
            #    costo_corrente += self._costo
            #    valore_corrente += self._valore_ottimo
            #    for id_tour,attrazioni in self._tour_attrazioni.items():
            #        attrazioni_usate = self.attrazioni_map[id_tour]
            self._ricorsione (start_index+1,pacchetto_parziale,durata_corrente,costo_corrente,valore_corrente,attrazioni_usate)

        """ Algoritmo di ricorsione che deve trovare il pacchetto che massimizza il valore culturale"""

        # TODO: è possibile cambiare i parametri formali della funzione se ritenuto opportuno
