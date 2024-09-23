from PyQt5.QtWidgets import QMenu, QAction
from qgis._core import QgsVectorLayer
from qgis._gui import QgsLayerTreeView, QgsMapCanvas

from attributeDialog import AttributeDialog


class LayerTreeViewMenu:
    def __init__(self, layerTreeView: QgsLayerTreeView, mapCanvas: QgsMapCanvas):
        # print(type(self))
        self.layerTreeView = layerTreeView
        self.default_action = layerTreeView.defaultActions()
        self.initAction(layerTreeView, mapCanvas)
        self.initMenu()

    def initAction(self, layerTreeView, mapCanvas) -> None:
        # 图层默认右键
        self.action_properties = QAction("属性", layerTreeView)
        self.action_zoom_to_layer = self.default_action.actionZoomToLayers(mapCanvas)
        self.action_move_to_top = self.default_action.actionMoveToTop()
        self.action_move_to_bottom = self.default_action.actionMoveToBottom()
        self.action_remove_layer = self.default_action.actionRemoveGroupOrLayer()
        self.action_zoom_select_layer = self.default_action.actionZoomToSelection(mapCanvas)
        # 矢量图层右键
        self.action_openAttribute = QAction("打开属性表", layerTreeView)
        self.action_start_edit = QAction("开始编辑", layerTreeView)
        self.action_select = QAction("选择要素", layerTreeView)
        self.action_export = QAction("导出图层", layerTreeView)
        # 栅格图层右键
        self.action_visual_scale = QAction("设置图层可见等级", layerTreeView)

        # 没有图层时右键
        self.action_open_map = QAction("打开地图", layerTreeView)
        self.action_open_vector = QAction("打开矢量文件", layerTreeView)
        self.action_open_raster = QAction("打开栅格文件", layerTreeView)

    def initMenu(self) -> None:
        self.vector_menu = self.initVectorMenu()
        self.raster_menu = self.initRasterMenu()
        self.otherMenu = self.initOtherMenu()

    def initVectorMenu(self) -> QMenu:
        vectorMenu = QMenu()
        vectorMenu.addAction(self.action_openAttribute)
        vectorMenu.addAction(self.action_zoom_to_layer)
        vectorMenu.addAction(self.action_move_to_top)
        vectorMenu.addAction(self.action_move_to_bottom)
        vectorMenu.addAction(self.action_remove_layer)
        vectorMenu.addAction(self.action_start_edit)
        vectorMenu.addAction(self.action_select)
        vectorMenu.addAction(self.action_export)
        vectorMenu.addAction(self.action_zoom_select_layer)
        vectorMenu.addAction(self.action_properties)
        # self.actionShowAttributeDialog.triggered.connect(self.openAttributeTableTriggered)
        return vectorMenu

    def initRasterMenu(self) -> QMenu:
        rasterMenu = QMenu()
        rasterMenu.addAction(self.action_visual_scale)
        rasterMenu.addAction(self.action_properties)
        return rasterMenu

    def initOtherMenu(self) -> QMenu:
        otherMenu = QMenu()
        otherMenu.addAction(self.action_open_map)
        otherMenu.addAction(self.action_open_vector)
        otherMenu.addAction(self.action_open_raster)
        return otherMenu


