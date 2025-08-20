from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsProcessing,
    QgsField, QgsFields, QgsFeature,
    QgsGeometry, QgsWkbTypes,
    QgsCoordinateTransform
)
from qgis.PyQt.QtCore import QCoreApplication, QVariant

class Rules_3treesperbuilding(QgsProcessingAlgorithm):
    INPUT_BUILDINGS = 'INPUT_BUILDINGS'
    INPUT_TREES = 'INPUT_TREES'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()
    
    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_BUILDINGS,
                QCoreApplication.translate('GreenRatingAlgorithm', 'Strato di input (Edifici)'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_TREES,
                QCoreApplication.translate('GreenRatingAlgorithm', 'Strato di input (Alberi)'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                'OUTPUT_BUILDINGS',
                QCoreApplication.translate('GreenRatingAlgorithm', 'Output edifici')
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                'OUTPUT_TREES',
                QCoreApplication.translate('GreenRatingAlgorithm', 'Output alberi')
            )
        )


    def name(self):
        return 'Sub-Rules for 3 trees per building'

    def displayName(self):
        return QCoreApplication.translate('GreenRatingAlgorithm', 'Sub-Rules for 3 trees per building')

    def group(self):
        return QCoreApplication.translate('GreenRatingAlgorithm', 'Analisi Ambientale Urbana')

    def groupId(self):
        return 'analisi_ambientale_urbana'

    def createInstance(self):
        return Rules_3treesperbuilding()
    
    def processAlgorithm(self, parameters, context, feedback):
        buildings = self.parameterAsSource(parameters, self.INPUT_BUILDINGS, context)
        trees = self.parameterAsSource(parameters, self.INPUT_TREES, context)

        # Sink edifici
        sink_build, id_build = self.parameterAsSink(
            parameters,
            'OUTPUT_BUILDINGS',
            context,
            buildings.fields(),
            buildings.wkbType(),
            buildings.sourceCrs()
        )

        for f in buildings.getFeatures():
            sink_build.addFeature(f)

        # Sink alberi
        sink_tree, id_tree = self.parameterAsSink(
            parameters,
            'OUTPUT_TREES',
            context,
            trees.fields(),
            trees.wkbType(),
            trees.sourceCrs()
        )

        for f in trees.getFeatures():
            sink_tree.addFeature(f)

        return {
            'OUTPUT_BUILDINGS': id_build,
            'OUTPUT_TREES': id_tree
        }
"""
        #recupera gli strati degli edifici
        edifici_input = self.parameterAsSource(
            parameters,
            self.INPUT_BUILDINGS,
            context
        )
        feedback.pushInfo("Verifica dei layer di edifici...")

        if edifici_input is None:
            feedback.reportError("Errore: Impossibile caricare lo strato degli edifici.")
            return {}
        
        feedback.pushInfo("Layer di input caricati con successo.")

        #recupera gli strati degli alberi
        alberi_input = self.parameterAsSource(
            parameters,
            self.INPUT_TREES,
            context
        )
        feedback.pushInfo("Verifica dei layer degli alberi...")

        if alberi_input is None:
            feedback.reportError("Errore: Impossibile caricare lo strato degli alberi.")
            return {}
        
        feedback.pushInfo("Layer di input caricati con successo.")

        # Inizializza il layer di output
        (sink, result) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            edifici_input.fields(),
            edifici_input.wkbType(),
            edifici_input.sourceCrs(),
            alberi_input.fields(),
            alberi_input.wkbType(),
            alberi_input.sourceCrs()
        )

        return {self.OUTPUT: result}
"""