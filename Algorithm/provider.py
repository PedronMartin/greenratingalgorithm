from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .algorithm import GreenRatingAlgorithm # Importiamo il nostro algoritmo

class GreenRatingProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Inizializza il provider.
        """
        super().__init__()

    def loadAlgorithms(self):
        """
        Carica gli algoritmi del provider.
        """
        self.addAlgorithm(GreenRatingAlgorithm())

    def id(self):
        """
        Restituisce un ID univoco per il provider.
        """
        return 'green_rating'

    def name(self):
        """
        Restituisce il nome del provider per l'interfaccia.
        """
        return self.tr('Analisi Ambientale Urbana')

    def icon(self):
        """
        Restituisce l'icona del provider.
        """
        return QgsProcessingProvider.icon(self)
