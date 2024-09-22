from qgis.core import QgsApplication
from PyQt5.QtCore import Qt
from myWindow import MainWindow

if __name__ == '__main__':
    QgsApplication.setPrefixPath('E:\\QGIS\\bin', True)
    QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QgsApplication([], True)
    app.initQgis()
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
    app.exitQgis()
