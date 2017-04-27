'''
Класс ProxyBuffer представляет из себя виртуальный буфер для обмена общей для многих виджетов информацией
'''
from PyQt4.QtCore import *

class ProxyBuffer:
    VIEW_MODES = ('Passability', 'Simple', 'Events')    # Список допустимых значений режима работы со сценой
    def __init__(self, main):
        '''
        Конструктор прокси-буфера принимает один аргумент:
            main - ссылка на главное окно приложения
        '''
        self.MAIN = main			# Ссылка на главное окно
        self.CONFIG = main.CONFIG	# Ссылка на объект конфигураций
        self.SCALE = 3				# Текущий уровень масштабирования сцены
        self.TILE = QByteArray()    # Текущий активный тайл. По умолчанию - пустой массив байтов
        self.SIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])# Текущий размер тайла
        self.LAYER = 1.0            # Текущий активный слой
        self.VIEW_MODE = 'Simple'   # Триггер режимов работы со сценой
        self.DRAW_GRID = True       # Триггер отрисовки вспомогательной сетки
        self.DRAW_BACK = True       # Триггер отрисовки заднего фона сцены
#========== Методы установки атрибутов ==========
    def setActiveTile(self, pixmap):
        # Метод установки текущего активного тайла
        buffer = QBuffer(self.TILE)     # Создаем буфер
        buffer.open(QIODevice.WriteOnly)# Открываем буфер для записи
        pixmap.save(buffer, 'PNG')      # Сохраняем изображение в массив байтов
        buffer.close()                  # Закрываем буфер
        self.MAIN.TILE_VIEWER.setPixmap(pixmap.scaled(self.SIZE*2,self.SIZE*2)) # Помещаем изображение в TILE_VIEWER
    def setActualTilesize(self, factor):
        # Метод устанвки текущего активного слоя
        self.SIZE = int(self.CONFIG['EDITOR OPTIONS']['Tilesize'])//3*factor
        self.MAIN.TILESET_MANAGER.refresh() # Обновляем менеджер тайлсетов
    def setActiveLayer(self, value):
        # Метод установки текущего активного слоя
        self.LAYER = value
    def setScaleMode(self, value):
        # Метод установки текущего уровня масштабирования сцены
        self.SCALE = value
    def setViewMode(self, value):
        # Метод установки режима работы со сценой
        if value in self.VIEW_MODES:    self.VIEW_MODE = value
        else:   raise ValueError ('Illegal Scene View Mode value! Must be {}, but {} given.'.format(self.VIEW_MODES, value))
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