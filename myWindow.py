import os.path
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QVBoxLayout, QMenu, QAction, QDialog, QApplication, QStatusBar, \
    QLabel, QComboBox
from qgis.PyQt.QtWidgets import QMainWindow
from qgis._core import QgsLayerTreeModel, QgsRasterLayer, QgsVectorLayer, QgsLayerTreeNode, QgsMapLayer, \
    QgsVectorLayerCache, QgsCoordinateReferenceSystem, QgsMapSettings
from qgis._gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge, QgsLayerTreeView, QgsAttributeTableView, QgsGui, \
    QgsAttributeTableModel, QgsAttributeTableFilterModel
from qgis.core import QgsProject
from untitled import Ui_MainWindow
from data_control.dataControl import DataManager
from MenuControl import LayerTreeViewMenu
from attributeDialog import AttributeDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 设置窗体标题
        self.setWindowTitle("312205040222jpy")
        # 设置画布
        self.mapCanvas = QgsMapCanvas(self)
        h1 = QHBoxLayout(self.frame)
        h1.setContentsMargins(0, 0, 0, 0)
        h1.addWidget(self.mapCanvas)

        # 关联画布
        # 建立图层树与地图画布的桥接
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.mapCanvas, self)

        # 初始化图层树
        v1 = QVBoxLayout(self.dockWidgetContents)
        self.layerTreeView = QgsLayerTreeView(self)
        v1.addWidget(self.layerTreeView)
        # 设置图层树风格
        self.model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)  # 允许图层节点重命名
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)  # 允许图层拖拽排序
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)  # 允许改变图层节点可视性
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)  # 展示图例
        self.model.setAutoCollapseLegendNodes(10)  # 当节点数大于等于10时自动折叠
        self.layerTreeView.setModel(self.model)
        self.connectFunc()
        self.control = LayerTreeViewMenu(self.layerTreeView, self.mapCanvas)

        self.layerTreeView.customContextMenuRequested.connect(self.showLayerTreeViewContextMenu)
        self.layerTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.control.action_openAttribute.triggered.connect(self.openAttributeTableTriggered)
        self.control.action_open_raster.triggered.connect(self.openRasterTriggered)
        self.control.action_open_vector.triggered.connect(self.openVectorTriggered)
        self.control.action_open_map.triggered.connect(self.actionOpenMapTriggered)

        self.mapCanvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
        # 状态栏控件
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('color: black; border: none')
        self.statusXY = QLabel('{:<40}'.format(''))  # x y 坐标状态
        self.statusBar.addWidget(self.statusXY, 1)
        self.statusScaleLabel = QLabel('比例尺')
        self.statusScaleComboBox = QComboBox(self)
        self.statusScaleComboBox.setFixedWidth(120)
        self.statusScaleComboBox.addItems(
            ["1:500", "1:1000", "1:2500", "1:5000", "1:10000", "1:25000", "1:100000", "1:500000", "1:1000000"])
        self.statusScaleComboBox.setEditable(True)
        self.statusBar.addWidget(self.statusScaleLabel)
        self.statusBar.addWidget(self.statusScaleComboBox)
        self.statusCrsLabel = QLabel(
            f"坐标系: {self.mapCanvas.mapSettings().destinationCrs().description()}-{self.mapCanvas.mapSettings().destinationCrs().authid()}")
        self.statusBar.addWidget(self.statusCrsLabel)
        self.setStatusBar(self.statusBar)
        self.mapCanvas.destinationCrsChanged.connect(self.showCrs)
        self.mapCanvas.xyCoordinates.connect(self.showXY)
        self.mapCanvas.scaleChanged.connect(self.showScale)
        self.statusScaleComboBox.editTextChanged.connect(self.changeScaleForString)

    def actionOpenMapTriggered(self):
        """
        打开地图响应槽函数
        :return:None
        """
        map_file, ext = QFileDialog.getOpenFileName(self, '打开', '',
                                                    "QGISMap(*.qhz);;All Files(*);;Other(*.gbkg;*.geojson;*.kml)")
        QgsProject.instance().read(map_file)

    def openRasterTriggered(self):
        """
        打开栅格文件响应槽函数
        :return: None
        """
        data_file, ext = QFileDialog.getOpenFileName(self, 'Open Raster', '', "QGIS Raster(*.tif)")
        # rasterLayer = QgsRasterLayer(data_file, os.path.basename(data_file))
        # QgsProject.instance().addMapLayer(rasterLayer)
        cur_raster = DataManager.readRasterFile(data_file)
        DataManager.addMapLayer(cur_raster, self.mapCanvas)

    def openVectorTriggered(self):
        """
        打开矢量文件响应槽函数
        :return: None
        """
        data_file, ext = QFileDialog.getOpenFileName(self, 'Open Vector', '', "QGIS Vector(*.shp)")
        # vectorLayer = QgsVectorLayer(data_file, os.path.basename(data_file))
        # QgsProject.instance().addMapLayer(vectorLayer)
        cur_vector = DataManager.readVectorFile(data_file)
        DataManager.addMapLayer(cur_vector, self.mapCanvas)

    def showLayerTreeViewContextMenu(self, index):
        selected_nodels: list[QgsLayerTreeNode] = self.layerTreeView.selectedLayerNodes()
        selected_layers: list[QgsMapLayer] = self.layerTreeView.selectedLayers()
        if len(selected_nodels) == 0:
            self.control.otherMenu.exec_(QCursor.pos())
        else:
            pass
        if len(selected_layers) == 1:
            # self.defaultMenu.exec_(QCursor.pos())
            current_layer = selected_layers[0]
            if (isinstance(current_layer, QgsVectorLayer)):
                self.control.vector_menu.exec_(QCursor.pos())
            elif (isinstance(current_layer, QgsRasterLayer)):
                self.control.raster_menu.exec_(QCursor.pos())
        else:
            pass

    def showContextMenu(self, index):
        contextMenu = QMenu(self)

        contextMenu.addAction(self.actionOpen_Map)
        contextMenu.addAction(self.actionOpen_Raster)
        contextMenu.addAction(self.actionOpen_Vector)

        action_quit = QAction("退出", self)
        contextMenu.addAction(action_quit)
        action_quit.triggered.connect(QApplication.quit)
        contextMenu.exec(QCursor.pos())

    def initAction(self) -> None:
        # 图层默认右键
        self.default_action = self.layerTreeView.defaultActions()
        self.action_properties = QAction("属性", self.layerTreeView)
        self.action_zoom_to_layer = self.default_action.actionZoomToLayers(self.mapCanvas)
        self.action_move_to_top = self.default_action.actionMoveToTop()
        self.action_move_to_bottom = self.default_action.actionMoveToBottom()
        self.action_remove_layer = self.default_action.actionRenameGroupOrLayer()
        # 矢量图层右键
        self.action_openAttribute = QAction("打开属性表", self.layerTreeView)
        self.action_start_edit = QAction("开始编辑", self.layerTreeView)
        self.action_select = QAction("选择要素", self.layerTreeView)
        self.action_export = QAction("导出图层", self.layerTreeView)
        # 栅格图层右键
        self.action_visual_scale = QAction("设置图层可见等级", self.layerTreeView)

        # 没有图层时右键
        self.action_open_map = QAction("打开地图", self.layerTreeView)
        self.action_open_vector = QAction("打开矢量文件", self.layerTreeView)
        self.action_open_raster = QAction("打开栅格文件", self.layerTreeView)

    def connectFunc(self):
        """
        绑定相关菜单栏或者工具栏按钮
        :return:
        """
        # 打开栅格数据
        self.actionOpen_Raster.triggered.connect(self.openRasterTriggered)
        # 打开矢量数据
        self.actionOpen_Vector.triggered.connect(self.openVectorTriggered)
        # 打开地图
        self.actionOpen_Map.triggered.connect(self.actionOpenMapTriggered)

    def openAttributeTableTriggered(self):
        # print(type(self.layerTreeView.currentLayer()))
        self.layer: QgsVectorLayer = self.layerTreeView.currentLayer()
        ad = AttributeDialog(self, self.layer)
        ad.show()

    def showCrs(self):
        mapSetting: QgsMapSettings = self.mapCanvas.mapSettings()
        self.statusCrsLabel.setText(
            f"坐标系: {mapSetting.destinationCrs().description()}-{mapSetting.destinationCrs().authid()}")

    def showXY(self, point):
        x = point.x()
        y = point.y()
        self.statusXY.setText(f'{x:.6f}, {y:.6f}')

    def showScale(self, scale):
        self.statusScaleComboBox.setEditText(f"1:{int(scale)}")

    def changeScaleForString(self, str):
        try:
            left, right = str.split(":")[0], str.split(":")[-1]
            if int(left) == 1 and int(right) > 0 and int(right) != int(self.mapCanvas.scale()):
                self.mapCanvas.zoomScale(int(right))
                self.mapCanvas.zoomWithCenter()
        except:
            print(traceback.format_stack())
