import os.path

from qgis._core import QgsProject, QgsMapLayer, QgsRasterLayer, QgsVectorLayer
from qgis._gui import QgsMapCanvas


# CUR_PROJECT = QgsProject.instance()


class DataManager:
    @classmethod
    def addMapLayer(cls, layer: QgsMapLayer, mapCanvas: QgsMapCanvas, firstAddLayer=False):
        """
        将一个有效的图层添加到当前的项目当中，并显示在地图画布当中
        :param layer: 有效的地图图层
        :param mapCanvas: 地图画布
        :param firstAddLayer: 判断是否是第一个图层
        :return: None
        """
        if layer is not None and layer.isValid():
            if (len(QgsProject.instance().mapLayers()) == 0):
                mapCanvas.setDestinationCrs(layer.crs())
                mapCanvas.setExtent(layer.extent())
            while QgsProject.instance().mapLayersByName(layer.name()):
                layer.setName(layer.name() + "_1")

            QgsProject.instance().addMapLayer(layer)
            layers = [layer] + [QgsProject.instance().mapLayer(i) for i in QgsProject.instance().mapLayers()]

            mapCanvas.setLayers(layers)
            mapCanvas.refresh()

    @classmethod
    def readRasterFile(cls, filePath: str):
        """
        读取栅格数据文件并封装成一个对象
        :param filePath: 文件路径
        :return: QgsRasterLayer对象
        """
        if os.path.exists(filePath):
            rasterLayer = QgsRasterLayer(filePath, os.path.basename(filePath))
            return rasterLayer
        else:
            return None

    @classmethod
    def readVectorFile(cls, filePath: str):
        """
        读取矢量数据文件并封装成一个对象
        :param filePath: 文件路径
        :return: QgsVectorLayer对象
        """
        if os.path.exists(filePath):
            vectorLayer = QgsVectorLayer(filePath, os.path.basename(filePath))
            return vectorLayer
        else:
            return None
