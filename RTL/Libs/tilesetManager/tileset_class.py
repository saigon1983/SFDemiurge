'''
В этом модуле описывается класс представления тайлсета, являющийся наследником класса QGraphicsScene
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.helpFunctions.adjust_to_tilesize import adjustToTilesize

class Tileset(QGraphicsScene):
    def __init__(self, main, pixmap):
        super().__init__()	# Инициализируем суперкласс
        self.config(main)	# Запускаем метод установки необходимых атрибутов
        self.setup(pixmap)	# Запускаем метод настройки виджета
    def config(self, main):
        # Метод установки необходимых атрибутов
        self.CONFIG = main.CONFIG	# Ссылка на объект конфигурации
        self.PROXY = main.PROXY		# Ссылка на прокси-буфер
        self.TILESIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])	# Фиксируем основной размер тайлов
    def setup(self, pixmap):
        # Метод настройки виджета
        self.image = pixmap                                         # Сохраняем изображение сцены в атрибуте
        item = QGraphicsPixmapItem(pixmap)							# Создаем объект сцены как экземпляр QGraphicsPixmapItem
        item.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)	# Устанавливаем контур сцены
        self.addItem(item)											# Размещаем тайлсет на сцене в виде самостоятельного объекта
        self.selectorCoords = QPoint(0,0)                           # Положение верхнего левого угла курсора выбора тайла
    def refresh(self):
        # Метод обновления сцены
        # Обновляем положение рамки выбора тайла
        self.setSelectorPosition(adjustToTilesize(self.selectorCoords, self.PROXY.SIZE))
    def drawBackground(self, painter, rect):
        # Перегружаем метод отрисовки заднего фона. В качестве него рисуется сетка темная сетка
        brush = QBrush()                    # Создаем кисть
        brush.setTexture(QPixmap('RTL\\Images\\Backgrounds\\ti_{}_bb.png'.format(self.TILESIZE)))	# Загружаем текстуру
        painter.setBrush(brush)				# Устанавливаем кисть
        painter.drawRect(self.sceneRect())  # Рисуем фон
    def drawForeground(self, painter, rect):
        # Перегружаем метод отрисовки переднего фона, чтобы отображать рамку выбора тайла
        pen = QPen()						# Создаем перо
        pen.setWidth(2)						# Задаем толщину рамки
        pen.setColor(Qt.yellow)				# Задаем цвет рамки
        pen.setJoinStyle(Qt.MiterJoin)		# Задаем метод сочленения линий рамки
        painter.setPen(pen)				    # Устанавливаем перо
        sidesize = self.PROXY.SIZE          # Получаем размер актуального тайла
        painter.drawRect(QRect(self.selectorCoords.x()+1,  self.selectorCoords.y()+1,
                               sidesize-2, sidesize-2))# Рисуем рамку
    def setSelectorPosition(self, newPosition):
        # Метод установки рамки выбора тайла в новую позицию newPosition
        self.selectorCoords = newPosition
        # Обновляем сцену
        self.update()
