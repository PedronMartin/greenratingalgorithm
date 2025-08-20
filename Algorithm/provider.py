from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from .algorithm import GreenRatingAlgorithm
from .Rules_tree import Rules_3treesperbuilding

class GreenRatingProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()

    def loadAlgorithms(self):
        self.addAlgorithm(GreenRatingAlgorithm())
        self.addAlgorithm(Rules_3treesperbuilding())
        # Aggiungi qui gli altri algoritmi se ne avrai in futuro

    def id(self):
        """
        Restituisce un ID univoco per il provider.
        """
        return 'green_rating'

    def name(self):
        """
        Restituisce il nome del provider per l'interfaccia.
        """
        return self.tr('Analisi Ambientale Urbana: 3-30-300')

    def icon(self):
        """
        Restituisce l'icona del provider.
        """
        # Se hai un'icona personalizzata per il provider, la dichiari qui.
        return QgsProcessingProvider.icon(self)
        
    """probabilmente aggiungeremo la possibilità di analizzare una zona geografica sulla base di una sola delle 3 caratteristiche 3-30-300"""