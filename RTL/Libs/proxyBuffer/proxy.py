'''
Класс ProxyBuffer представляет из себя виртуальный буфер для обмена общей для многих виджетов информацией
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from RTL.Libs.sceneManager.scene_tile import Tile
import math

class ProxyBuffer:
    VIEW_MODES = ('Passability', 'Simple', 'Events')    # Список допустимых значений режима работы со сценой
    def __init__(self, main):
        '''
        Конструктор прокси-буфера принимает один аргумент:
            main - ссылка на главное окно приложения
        '''
        self.MAIN = main			# Ссылка на главное окно
        self.CONFIG = main.CONFIG	# Ссылка на объект конфигураций
        # Уровень масштабирования сцены. Может принимать значения от 0 до 4 включительно. Масштаб 1:1 соответствует
        # значению 3 (по умолчанию)
        self.SCALE = 3
        # Текущий активный тайл. Представляет из себя список тайлов, который может содержать от 1 до 9 элементов
        self.TILE = []
        # Текущий размер тайла. По умолчанию присваивается значение из файла конфигураций
        self.SIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])
        # Минимальный размер тайла. Определяется как 1/3 от максимального размера из файла конфигураций
        self.BASESIZE = self.SIZE//3# Фиксируем минимальный размер тайла
        # Значение текущего активного слоя. Может принимать только значения типа float. Используется для корректной
        # отрисовки сцены - каждый добавляемый элемент будет иметь высоту отрисовки, равную этому значению
        self.LAYER = 1.0
        # Триггер отрисовки сцены. Может иметь три положения: Whole, Active, Transparent. Whole - все слои сцены
        # отрисовываются на отображении. Active - отрисовывается только активный слой, остальные скрыты, Transparent -
        # четко отрисовывается только активный слой, остальные - полупрозрачные
        self.DRAW_MODE = 'Whole'
        # Тригеер режимов работы со сценой. Значение Simple означает стандартный режим редактирования. Passability -
        # сцена отображает карту проходимости. Events - сцена находится в режиме редактирования событий
        self.VIEW_MODE = 'Simple'
        # Триггер отрисовки вспомогательной сетки
        self.DRAW_GRID = True
        # Триггер отрисовки заднего фона сцены
        self.DRAW_BACK = True
#========== Методы установки атрибутов ==========
    def setActiveTile(self, pixArray):
        # Метод установки текущего активного тайла
        self.TILE.clear()                       # Очищаем массив
        self.MAIN.TILE_VIEWER.clear()           # Очищаем содержимое TILE_VIEWER
        pixmap = QPixmap(self.SIZE, self.SIZE)  # Создаем прообраз изображения тайла для TILE_VIEWER
        pixmap.fill(Qt.magenta)                 # Заполняем его магическим цветом
        painter = QPainter(pixmap)              # Включаем рисование на прообразе
        for pix in pixArray:                    # Запускаем цикл обработки
            # ====== Заполнение массива массивами данных ======
            byteArray = QByteArray()            # Задаем массив байтов
            buffer = QBuffer(byteArray)         # Создаем буфер
            buffer.open(QIODevice.WriteOnly)    # Открываем буфер для записи
            pix.save(buffer, 'PNG')             # Сохраняем изображение в массив байтов
            buffer.close()                      # Закрываем буфер
            # ====== Создание отображения тайла ======
            size    = math.sqrt(len(pixArray))  # Размер стороны квадрата в минимальных тайлах
            index   = pixArray.index(pix)       # Индекс текущего изображения в массиве изображений
            x = self.BASESIZE * (index % size)  # Координата x
            y = self.BASESIZE * (index // size) # Координата y
            rect = QRect(QPoint(x, y), QSize(self.BASESIZE, self.BASESIZE))     # Определяем координаты прямоугольника
            painter.drawPixmap(rect, pix, pix.rect())                           # Рисуем рисунок pix на рисунок pixmap
            self.TILE.append(Tile(byteArray, x, y))                             # Добавляем тайл в массив
        painter.end()                           # Выключаем отрисовщик
        self.MAIN.TILE_VIEWER.setPixmap(pixmap.scaled(self.SIZE*2,self.SIZE*2)) # Помещаем изображение в TILE_VIEWER
    def setActualTilesize(self, factor):
        # Метод устанвки текущего активного слоя
        self.SIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])//3*factor
        self.MAIN.TILESET_MANAGER.refresh() # Обновляем менеджер тайлсетов
        self.MAIN.SCENE_MANAGER.refresh()
    def setActiveLayer(self, value):
        # Метод установки текущего активного слоя
        self.LAYER = float(value)
        self.MAIN.SCENE_MANAGER.activeLayerChanged()
    def setScaleMode(self, value):
        # Метод установки текущего уровня масштабирования сцены
        self.SCALE = value
    def setViewMode(self, value):
        # Метод установки режима работы со сценой
        if value in self.VIEW_MODES:    self.VIEW_MODE = value
        else:   raise ValueError ('Illegal Scene View Mode value! Must be {}, but {} given.'.format(self.VIEW_MODES, value))
    def switchDrawScene(self, value):
        # Метод смены режима отображения слоев сцены
        if value == 'W':    self.DRAW_MODE = 'Whole'
        elif value == 'A':  self.DRAW_MODE = 'Active'
        elif value == 'T':  self.DRAW_MODE = 'Transparent'
        self.MAIN.SCENE_MANAGER.scene().activeLayerChanged()
    def switchViewMode(self):
        # Метод автоматического переключения режимов работы со сценой
        if self.VIEW_MODE == 'Passability': self.setViewMode('Simple')
        else:							    self.setViewMode('Passability')
        self.MAIN.BARS.updateGridPass(self.VIEW_MODE, self.DRAW_GRID)
        self.MAIN.SCENE_MANAGER.refresh()
    def switchDrawGrid(self):
        # Метод переключения режима отриосвки сетки
        self.DRAW_GRID = not self.DRAW_GRID
        self.MAIN.BARS.updateGridPass(self.VIEW_MODE, self.DRAW_GRID)
        self.MAIN.SCENE_MANAGER.refresh()
    def switchDrawBack(self):
        # Метод переключения режима отрсио
        self.DRAW_BACK = not self.DRAW_BACK
        self.MAIN.SCENE_MANAGER.refresh()