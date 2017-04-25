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
        self.TILESIZE = int(self.mainWindow.CONFIG['EDITOR OPTIONS']['Tilesize'])   # Базовый размер тайла
        self.setMinimumSize((self.TILESIZE + 1) * 20, self.TILESIZE * 20 + 5)	    # Минимальный размер
        self.PROXY = self.mainWindow.PROXY					# Ссылка на прокси-буфер
        self.sceneBuffer = None                             # Буфер для сцен, куда они помещаются при изменении
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
        # Задаем контейнеры для сцен, чтобы использовать методы undo() и redo()
        self.pastScenes  	= []  		# Контейнер прошлых сцен. Для UNDO
        self.futureScenes	= []  		# Контейнер будущих сцен. Для REDO
        self.STACKSIZE = int(self.mainWindow.CONFIG['EDITOR OPTIONS']['Undo stacksize'])    # Размер стека для UNDO
        self.sceneChanged = False       # Триггер измененности сцены. Если сцена меняется, устанавливается True
    def scaleChange(self):
        # Метод смены масштабирования
        delta = [0.25, 0.5, 1, 2, 4][self.PROXY.SCALE] 				# Выбираем масштаб в зависимости от положения ползунка масштабирования
        self.setTransform(QTransform(QMatrix(delta,0,0,delta,0,0))) # Устанавливаем масштаб
#==========Методы изменения состояния сцены и состояния триггеров==========
    def refresh(self):
        # Метод обновления виджета
        self.scene().update()
    def setMouseButtonsFlags(self, event):
        # Метод меняет флаги нажатия кнопок мыши
        if event.button() 	== Qt.LeftButton and not self.mouseRightPressed:
            self.mouseLeftPressed = True
        if event.button() 	== Qt.RightButton and not self.mouseLeftPressed:
            self.mouseRightPressed = True
    def switchDrawGrid(self):
        # Метод переключения режима отрисовки сетки
        self.scene().drawFG = not self.scene().drawFG
        self.refresh()
    def switchDrawPass(self):
        # Метод переключения режима отображения проходимости
        if self.scene().viewMode == 'Passability': self.scene().viewMode = 'Simple'
        else:														self.scene().viewMode = 'Passability'
        self.refresh()
    def setScene(self, scene):
        # Переопределяем метод установки новой сцены
        super().setScene(scene)	                                        # Вызываем метод суперкласса
        tilsetList = self.mainWindow.TILESET_SELECTOR.tilesetData.NAMES # Получаем список доступных тайлсетов
        index = tilsetList.index(self.scene().tileset)                  # Получаем индекс базового тайлсета сцены в этом списке
        self.mainWindow.TILESET_SELECTOR.setCurrentIndex(index)         # Автоматически настраиваем виджет на отображение базового тайлсета
        self.scene().tileChanged.connect(self.onChange)                 # Соединяем сигнал об изменении сцены с слотом
        self.sceneChanged = False                                       # Отключаем триггер изменения сцены
#==========Методы размещения обектов==========
    def onChange(self):
        # Слот, вызываемый при изменении сцены. Включает триггер
        if not self.sceneChanged: self.sceneChanged = True
    def getTilesInRect(self, coords):
        # Метод возвращает список тайлов, которые пересекаются с прямоугольником размером с текущий размер тайла
        correctedCoords = adjustToTilesize(coords, self.PROXY.SIZE)
        rectangleToUse  = QRectF(QPointF(correctedCoords),QSizeF(self.PROXY.SIZE, self.PROXY.SIZE))
        return self.scene().items(rectangleToUse)
    def placeTile(self, coords, tiles):
        # Метод размещает текущий активный тайл на текущей сцене в координатах coords
        if self.PROXY.TILE: # Размещаем тайл только при наличии этого тайла в буфере
            pointToPlace = adjustToTilesize(coords, self.PROXY.SIZE)    # Корректируем координаты
            xyz = (pointToPlace.x(), pointToPlace.y(), self.PROXY.LAYER)# Собираем в кортеж координаты и высоту
            newTile = Tile(self.PROXY.TILE[:], *xyz)                    # Конструируем тайл
            # Перебираем тайлы под курсором, и если находим такой же тайл на той же высоте, выходим из метода
            for tile in tiles:
                if tile.zValue() == self.PROXY.LAYER and tile == newTile: return
            # Повторно перебираем тайлы и удаляем те, которые находятся на текущием слое
            for tile in tiles:
                if tile.zValue() == self.PROXY.LAYER: self.scene().removeItem(tile)
            self.futureScenes.clear()       # Очищаем контейнер будущих сцен
            self.scene().placeTile(newTile) # Передаем тайл сцене
    def removeTile(self, coords, tiles):
        # Метод удаления тайлов в текущих координатах
        sameLevelTiles = [tile for tile in tiles if tile.zValue() == self.PROXY.LAYER]
        if sameLevelTiles:
            for tile in sameLevelTiles:
                if tile.zValue() == self.PROXY.LAYER: self.scene().removeTile(tile)
        self.futureScenes.clear()       # Очищаем контейнер будущих сцен
    def mouseInScene(self, coords):
        # Метод проверяет, находится ли курсор мыши в активной зоне сцены (можно ли рисовать)
        if coords.x() >= 0 and coords.y() >= 0 and coords.x() < self.scene().width() and coords.y() < self.scene().height(): return True
        return False
#==========Методы преобразовния величин и проверок состояния==========
    def mapToCells(self, coords):
        # Статический метод преобразования координат курсора в координаты сетки размером TILESIZE
        x = int(coords.x())//self.TILESIZE + 1
        y = int(coords.y())//self.TILESIZE + 1
        return (x, y)
    def showMousePosition(self, event):
        # Метод отображения координат мыши на сцене в строке состояния
        coords = self.mapToScene(event.x(),event.y())   		# Получаем коориднаты
        if self.mouseOverWidget and self.mouseInScene(coords):	# Если курсор находится в зоне видимости и в зоне отрисовки - выводим координаты
            x, y = self.mapToCells(coords)
            self.mainWindow.STATUSBAR.showMessage('{}:{}'.format(x, y))
        else: self.mainWindow.STATUSBAR.clearMessage()		    # В противном случае очищаем координаты на статусбаре
#==========Методы, относящиеся к применению команд UNDO и REDO==========
    def memorizeScene(self):
        # Метод запоминает текущее состояние сцены и добавляет его в контейнер pastScenes
        if len(self.pastScenes) >= self.STACKSIZE: self.pastScenes.pop(0)   # Удаляем первый элемент контейнера, если его размер превысил допустимый
        if self.sceneBuffer: self.pastScenes.append(self.sceneBuffer) 		# Добавляем текущую сцену в контейнер
        self.mainWindow.BARS.updateUndoRedo()
    def rememberScene(self):
        # Метод запоминает текущее состояние сцены и добавляет его в контейнер futureScenes. Поскольку в этот контейнер
        # попадают исключительно те сцены, которые были в контейнере pastScenes, нет необходимости задавать ему размер
        self.futureScenes.append(self.scene().duplicate())   # Добавляем текущую сцену в контейнер
        self.mainWindow.BARS.updateUndoRedo()
    def setPreviousScene(self):
        # Метод установки предыдущей сцены, вместо текущей при использовании UNDO
        if self.pastScenes and self.scene().viewMode == 'Simple':   # Запускаем только, если контейнер предыдущих состояний не пустой
            self.rememberScene()                                    # Сохраняем текущую сцену в будущие сцены
            self.setScene(self.pastScenes.pop())                    # Вытаскиваем последнее состояние из контейнера и устанавливаем его
            self.scene().unsaved()                                  # Уведомляем сцену, что она не сохранена
            self.mainWindow.BARS.updateUndoRedo()
    def setFutureScene(self):
        # Метод установки будущей сцены, вместо текущей при использовании REDO
        if self.futureScenes and self.scene().viewMode == 'Simple': # Запускаем только, если контейнер будущих состояний не пустой
            self.pastScenes.append(self.scene().duplicate())        # Сохраняем текущую сцену в прошлые сцены
            self.setScene(self.futureScenes.pop())                  # Вытаскиваем последнее состояние из контейнера и устанавливаем его
            self.scene().unsaved()                                  # Уведомляем сцену, что она не сохранена
            self.mainWindow.BARS.updateUndoRedo()
#==========Методы реакции на пользоватльский ввод (движения/нажатия мыши/клавиатуры)==========
    def enterEvent(self, event):
        # Перехватываем события входа курсора мыши в зону виджета
        self.mouseOverWidget   = True   # Фиксируем, переключая триггер
        return super().enterEvent(event)
    def leaveEvent(self, event):
        # Перехватываем события выхода курсора мыши из зоны виджета
        self.mouseOverWidget   = False  # Выключаем триггер
        self.mainWindow.STATUSBAR.clearMessage()  # Очищаем строку состояния
        return super().leaveEvent(event)
    def mousePressEvent(self, event):
        # Метод обработки события нажатия кнопок мыши
        self.setMouseButtonsFlags(event) 		        # Выставляем значение истины для одной из нажатых кнопок мыши
        coords = self.mapToScene(event.x(),event.y())   # Получаем координаты текущего местоположения курсора мыши
        if self.scene() and self.mouseInScene(coords):  # Если курсор находится в допустимых координатах и вообще есть сцена
            # Обработка нажатий кнопок мыши для состояния редактирвоания сцены Simple
            self.sceneBuffer = self.scene().duplicate() # Запоминаем текущее состояние в буфер
            if self.scene().viewMode == 'Simple':
                collideTiles = self.getTilesInRect(coords)  # Получаем список пересекающихся тайлов
                # Обрабатываем нажатие левой кнопки. По сути, передаем управление методу установки тайла и решения принимает он
                if self.mouseLeftPressed:                       self.placeTile(coords, collideTiles)
                # Обрабатываем нажатие правой кнопки мыши. При отсутствии тайлов - пропускаем сигнал нажатия
                elif self.mouseRightPressed and collideTiles:   self.removeTile(coords, collideTiles)
    def mouseMoveEvent(self, event):
        self.showMousePosition(event)	# Выводим координаты текущей клетки под курсором в строку состояния
        if self.mouseLeftPressed or self.mouseRightPressed:	# Если нажата одна из нопок мыши
            coords = self.mapToScene(event.x(),event.y())   # Получаем координаты текущего местоположения курсора мыши
            # Обработка нажатий кнопок мыши для состояния редактирвоания сцены Simple
            if self.scene().viewMode == 'Simple':
                collideTiles = self.getTilesInRect(coords)  # Получаем список пересекающихся тайлов
                # Обрабатываем нажатие левой кнопки. По сути, передаем управление методу установки тайла и решения принимает он
                if self.mouseLeftPressed:                       self.placeTile(coords, collideTiles)
                # Обрабатываем нажатие правой кнопки мыши. При отсутствии тайлов - пропускаем сигнал нажатия
                elif self.mouseRightPressed and collideTiles:   self.removeTile(coords, collideTiles)
    def mouseReleaseEvent(self, event):
        # Метод обработки события отпускания кнопок мыши
        if event.button() == Qt.RightButton:        self.mouseRightPressed  = False
        if event.button() == Qt.LeftButton:         self.mouseLeftPressed   = False
        if self.sceneChanged and self.sceneBuffer:  self.memorizeScene()
        self.sceneBuffer    = None
        self.sceneChanged   = False