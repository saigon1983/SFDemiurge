'''
Виджет отображения текущего тайлсета и взаимодействия с ним
'''
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
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
    # Добавляем в массив виды сцен, иготовленные на основе нарезки
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
