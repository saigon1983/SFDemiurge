'''
Виджет отображения текущего тайлсета и взаимодействия с ним
'''
import os
from RTL.Libs.tilesetManager.tileset_class import *

def sliceFromImage(main, tilesetData):
    # Функция "нарезки" тайлсетов из файла изображения согласно действующим правилам
    file 	= tilesetData.setdefault('File', r'RTP\Tilesets\TestTilesetO.png')	# Получаем путь к файлу или путь по умолчанию
    line 	= int(tilesetData.setdefault('Line', 432))							# Получаем координаты линии разреза или значение по умоолчанию
    if not os.path.isfile(file): raise ValueError('No such tileset file {}!'.format(file))			# Проверяем валидность файла
    views = []																								# Кортеж для всех видов, нарезанных из файла
    # Производим нарезку на графические сцены Tileset
    pixmap = QPixmap(file)
    scene_A = Tileset(main, pixmap.copy(0, 0, pixmap.width(), line))
    scene_B = Tileset(main, pixmap.copy(0, line, pixmap.width(), pixmap.height()-line))
    # Добавляем в массив виды сцен, изготовленные на основе нарезки
    views.append(TilesetViewer(scene_A))
    views.append(TilesetViewer(scene_B))
    # Возвращаем массив
    return views

class TilesetViewer(QGraphicsView):
    '''
    Класс описывает интерфейс взаимодействия пользователя с объектом тайлсета
    '''
    def __init__(self, scene):
        super().__init__(scene)	# Инициализируем суперкласс
        self.config()			# Запускаем метод установки необходимых атрибутов
        self.setup()			# Запускаем метод настройки виджета
    def config(self):
        # Метод установки атрибутов
        self.PROXY = self.scene().PROXY
        self.TILESIZE = self.scene().TILESIZE
        self.TILES_IR = int(self.scene().CONFIG['EDITOR OPTIONS']['Tiles_in_row'])	# Ширина виджета в тайлах
        self.TILES_IC = int(self.scene().CONFIG['EDITOR OPTIONS']['Tiles_in_col'])	# Высота видимой части виджета в тайлах
    def setup(self):
        # Метод настройки виджета
        self.setMouseTracking(True)								# Подключаем слежение за мышью
        self.setFixedWidth(self.TILESIZE * self.TILES_IR*2+6)	# Фиксируем ширину отображения
        self.setFixedHeight(self.TILESIZE * self.TILES_IC*2)	# Фиксируем высоту отображения
        self.setAlignment(Qt.AlignHCenter | Qt.AlignTop)		# Выравниваем изображение по центру и по врехнему краю
        self.setTransformationAnchor(QGraphicsView.NoAnchor)	# Отключаем якорь отображения сцены
        self.setTransform(QTransform(QMatrix(2,0,0,2,0,0)))		# Запускает отображение в режиме двойного увеличения
        self.setVerticalScrollBarPolicy(1)						# Отключаем отображение вертикальной полосу прокрутки (прокрутка колесиком работает)
        self.setHorizontalScrollBarPolicy(1)					# Отключаем отображение горизонтальной полосы прокрутки
    def refresh(self):
        # Метод обновления виджета
        self.scene().refresh()
    def setActiveTile(self, coords = QPoint(0, 0), tilesize = None):
        # Метод выбора нового активного тайла
        coords      = coords
        tilesize    = tilesize
        if coords != QPoint(0, 0): coords = self.scene().selectorCoords # Фиксируем координаты рамки выбора
        if not tilesize: tilesize = self.PROXY.SIZE                     # Получаем актуальный размер тайла
        tileFrame = QRect(coords, QSize(tilesize, tilesize))           # Объект границ тайла
        tilePixmap = self.scene().image.copy(tileFrame)                 # Вырезаем изображение тайла согласно заданным границам
        self.PROXY.setActiveTile(tilePixmap)                            # Передаем изобрадение в прокси-буфер
    def mousePressEvent(self, event):
        # Перегружаем метод реакции на нажатие кнопок мыши. Виджет реагирует только на левую кнопку
        if event.button() == Qt.LeftButton:
            tileSize = self.PROXY.SIZE
            coords   = adjustToTilesize(self.mapToScene(event.pos()), tileSize)
            if self.mouseInScene(coords):
                self.scene().setSelectorPosition(coords)
                self.setActiveTile(coords, tileSize)
    def mouseInScene(self, coords):
        # Метод проверяет, находится ли курсор мыши в допустимых пределах вида
        if coords.y() < self.scene().height() and coords.x() >= 0 and coords.x() < self.scene().width(): return True
        return False