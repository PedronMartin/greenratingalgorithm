from qgis.core import QgsProcessingAlgorithm

class GreenRatingAlgorithm(QgsProcessingAlgorithm):
    def __init__(self):
        super().__init__()

    def name(self):
        return 'greenrating'

    def displayName(self):
        return 'Calcola Indice 3-30-300'

    def group(self):
        return 'Analisi Ambientale Urbana'

    def groupId(self):
        return 'analisi_ambientale'

    def createInstance(self):
        return GreenRatingAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        # Qui andrà il tuo algoritmo
        return {}
