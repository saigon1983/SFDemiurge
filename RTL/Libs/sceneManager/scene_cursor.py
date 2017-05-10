# В этом модуле описан класс рамки под курсором для виджета менеджера сцены
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.helpFunctions.adjust_to_tilesize import adjustToTilesize

class FrameCursor(QGraphicsPixmapItem):
    def __init__(self):
        # Конструктор класса всего лишь инициализирует суперкласс и проставляет высоту отрисовки
        super().__init__()
        self.setZValue(10.0)
    def move(self, coords, size):
        # Метод перемещения курсора. Меняет позицию в зависимости переданных координат и текущего размера тайла
        self.setPos(adjustToTilesize(coords, size))
    def setFrame(self, size):
        pixmap = QPixmap(QSize(size, size))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.white)
        painter.setPen(pen)
        painter.drawRect(QRect(QPoint(0,0), QSize(size, size)))
        painter.end()
        self.setPixmap(pixmap)