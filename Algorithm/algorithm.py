from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessing
)
from qgis.PyQt.QtCore import QCoreApplication

class GreenRatingAlgorithm(QgsProcessingAlgorithm):
    INPUT_BUILDINGS = 'INPUT_BUILDINGS'
    INPUT_TREES = 'INPUT_TREES'
    INPUT_GREEN_AREAS = 'INPUT_GREEN_AREAS'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_BUILDINGS,
                QCoreApplication.translate('GreenRatingAlgorithm', 'Strato di input degli edifici'),
                [QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_TREES,
                QCoreApplication.translate('GreenRatingAlgorithm', 'Strato di input degli alberi'),
                [QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_GREEN_AREAS,
                QCoreApplication.translate('GreenRatingAlgorithm', 'Strato di input delle aree verdi'),
                [QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                QCoreApplication.translate('GreenRatingAlgorithm', 'Risultato dell\'algoritmo')
            )
        )

    def name(self):
        return 'calcola_indice_3_30_300'

    def displayName(self):
        return QCoreApplication.translate('GreenRatingAlgorithm', 'Calcola Indice 3-30-300')

    def group(self):
        return QCoreApplication.translate('GreenRatingAlgorithm', 'Analisi Ambientale Urbana')

    def groupId(self):
        return 'analisi_ambientale_urbana'

    def createInstance(self):
        return GreenRatingAlgorithm()

    def processAlgorithm(self, parameters, context, feedback):
        # Recupera gli strati di input dall'interfaccia utente
        edifici_input = self.parameterAsSource(
            parameters,
            self.INPUT_BUILDINGS,
            context
        )

        feedback.pushInfo("Verifica dei layer di input...")

        if edifici_input is None:
            feedback.reportError("Errore: Impossibile caricare lo strato degli edifici.")
            return {}
        
        feedback.pushInfo("Layer di input caricato con successo.")

        # Inizializza il layer di output
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            edifici_input.fields(),
            edifici_input.wkbType(),
            edifici_input.sourceCrs()
        )

        # Inizializza il contatore di progresso
        total_features = edifici_input.featureCount()

        # Itera su ogni elemento (edificio) del layer di input e lo scrive nell'output
        for i, feature in enumerate(edifici_input.getFeatures()):
            if feedback.isCanceled():
                break
            
            # Aggiorna la barra di progresso
            feedback.setProgress(int((i / total_features) * 100))
            
            # Scrivi la feature nell'output
            sink.addFeature(feature)

        # Restituisce l'output
        return {self.OUTPUT: dest_id}