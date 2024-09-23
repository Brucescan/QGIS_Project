from PyQt5.QtWidgets import QDialog, QHBoxLayout
from qgis._core import QgsVectorLayer, QgsVectorLayerCache
from qgis._gui import QgsAttributeTableView, QgsGui, QgsAttributeTableModel, QgsAttributeTableFilterModel


class AttributeDialog(QDialog):
    def __init__(self, mainWindows, layer):
        # print(type(mainWindows))
        super(AttributeDialog, self).__init__(mainWindows)
        self.mainWindows = mainWindows
        self.mapCanvas = self.mainWindows.mapCanvas
        self.layer: QgsVectorLayer = layer
        self.setWindowTitle(self.layer.name() + "属性表")
        vl = QHBoxLayout(self)
        self.tableView = QgsAttributeTableView(self)
        self.resize(400, 400)
        vl.addWidget(self.tableView)
        self.openAttributeDialog()
        QgsGui.editorWidgetRegistry().initEditors(self.mapCanvas)

    def openAttributeDialog(self):
        self.layerCache = QgsVectorLayerCache(self.layer, 10000)
        self.tableModel = QgsAttributeTableModel(self.layerCache)
        self.tableModel.loadLayer()
        self.tableFilterModel = QgsAttributeTableFilterModel(self.mapCanvas, self.tableModel, parent=self.tableModel)
        self.tableFilterModel.setFilterMode(QgsAttributeTableFilterModel.ShowAll)  # 显示问题
        self.tableView.setModel(self.tableFilterModel)

