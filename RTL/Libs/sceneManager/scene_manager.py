'''
В этом модуле описан менеджер сцены - виджет, позволяющий выполнять все операции по редактированию сцены
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from RTL.Libs.helpFunctions.adjust_to_tilesize import adjustToTilesize
from RTL.Libs.sceneManager.scene_tile import Tile

class SceneManager(QGraphicsView):
    def __init__(self, main):
        self.mainWindow = main				# Ссылка на главное окно
        super().__init__(self.mainWindow)	# Инициализируем суперкласс
        self.setup()						# Запускаем настройку виджета
        self.setTriggers()                  # Запускаем натсройку триггеров
#==========Методы установки и настройки начального состояния==========
    def setup(self):
        # Метод настройки виджета
        self.basicTilseSize = int(self.mainWindow.CONFIG['EDITOR OPTIONS']['Tilesize'])	    # Базовый размер тайла
        self.setMinimumSize((self.basicTilseSize + 1) * 20, self.basicTilseSize * 20 + 5)	# Минимальный размер
        self.PROXY = self.mainWindow.PROXY					# Ссылка на прокси-буфер
        self.setMouseTracking(True)							# Виджет отслеживает положение мыши
        self.setDragMode(QGraphicsView.RubberBandDrag) 		# Вариант реакции на нажатие мыши
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)       # Точка (0, 0) сцены всегда отображается в левом верхнем углу
        self.setTransformationAnchor(QGraphicsView.NoAnchor)# Точка (0, 0) сцены всегда отображается в левом верхнем углу
        self.scaleChange()     								# Устанавливаем двойной зум по умолчанию
    def setTriggers(self):
        # Метод настройки триггеров и атрибутов
        self.mouseLeftPressed  	= False # Триггер нажатия левой  кнопки мыши
        self.mouseRightPressed 	= False # Триггер нажатия правой кнопки мыши
        self.mouseOverWidget   	= False # Нахождения мыши над виджетом
    def refresh(self):
        # Метод обновления виджета
        self.update()
    def scaleChange(self):
        # Метод смены масштабирования
        delta = [0.25, 0.5, 1, 2, 4][self.PROXY.SCALE] 				# Выбираем масштаб в зависимости от положения ползунка масштабирования
        self.setTransform(QTransform(QMatrix(delta,0,0,delta,0,0))) # Устанавливаем масштаб
    def setScene(self, scene):
        # Переопределяем метод установки новой сцены
        super().setScene(scene)	# Вызываем метод суперкласса
    def placeTile(self, coords):
        # Метод размещает текущий активный тайл на текущей сцене в координатах coords
        if self.PROXY.TILE:
            pointToPlace = adjustToTilesize(coords, self.PROXY.SIZE)
            newTile = Tile(self.PROXY.TILE, pointToPlace.x(), pointToPlace.y(), self.PROXY.LAYER)
            self.scene().placeTile(newTile)
    def mouseInScene(self, coords):
        # Метод проверяет, находится ли курсор мыши в активной зоне сцены (можно ли рисовать)
        if coords.x() >= 0 and coords.y() >= 0 and coords.x() < self.scene().width() and coords.y() < self.scene().height(): return True
        return False
    def setMouseButtonsFlags(self, event):
        # Метод меняет флаги нажатия кнопок мыши
        if event.button() 	== Qt.LeftButton and not self.mouseRightPressed:
            self.mouseLeftPressed = True
        if event.button() 	== Qt.RightButton and not self.mouseLeftPressed:
            self.mouseRightPressed = True
    def mousePressEvent(self, event):
        # Метод обработки события нажатия кнопок мыши
        self.setMouseButtonsFlags(event) 		 # Выставляем значение истины для одной из нажатых кнопок мыши
        coords = self.mapToScene(event.x(),event.y())# Получаем координаты текущего местоположения курсора мыши относительно сцены
        if self.scene() and self.mouseInScene(coords):
            if self.scene().viewMode == 'Simple':
                if self.mouseLeftPressed:
                    self.placeTile(coords)			# Размещаем активный тайл
    def mouseReleaseEvent(self, event):
        # Метод обработки события отпускания кнопок мыши
        if event.button() == Qt.RightButton:    self.mouseRightPressed  = False
        if event.button() == Qt.LeftButton:     self.mouseLeftPressed   = False
